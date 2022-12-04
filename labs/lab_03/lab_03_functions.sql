select *
from automobiles;

-- Скалярная функция
-- Значение цены с примением указанной скидки
create or replace function PriceSale(price int, sale int)
returns int as $$
begin
    return price * (1 - sale::real / 100);
end;
$$ language plpgsql;

select model, brand, price, PriceSale(price, 25)
from automobiles;

-- Подставляемая табличная функция
-- Автомобили с двигателем заданной мощности
create or replace function MakeTableAuEng(pw int)
returns table (brand varchar(30), model varchar(40), power int, capacity numeric(3, 1)) as $$
begin
    return query
    select au.brand, au.model , e.power, e.capacity
    from automobiles au join engines e on au.vin = e.vin
    where e.power = pw;
end;
$$ language plpgsql;

select *
from MakeTableAuEng(150);

-- Многооператорная табличная функция
-- Автомобили заданного бренда или заданного года производства
create or replace function GetAutosByBrandOrProdYear(str varchar(30), num int)
returns table (vin varchar(17), brand varchar(30), model varchar(40), prod_year int) as $$
begin
    return query
    select a.vin, a.brand, a.model, a.prod_year
    from automobiles as a
    where a.brand = $1;

    return query
    select a.vin, a.brand, a.model, a.prod_year
    from automobiles as a
    where a.prod_year = $2;
end;
$$ language plpgsql;

select *
from GetAutosByBrandOrProdYear('Nissan', 2000);

-- Рекурсивная функция или функция с рекурсивным ОТВ
create or replace function AgeSum(startId int, endId int)
returns int as $$
declare
     sum int;
begin
    if startId > endId then
        return 0;
    end if;
    select age
    into sum
    from customers
    where id = startId;
    return sum + AgeSum(startId + 1, endId);
end;
$$ language plpgsql;

select *
from AgeSum(1, 100);

select *
from customers;

-- Хранимая процедура
-- Обновление цены на заданный процент у указанного бренда
create or replace procedure UpdatePriceForBrand(proc int, br varchar(30))
as $$
begin
    update automobiles
    set price = price * (1 + proc::real / 100)
    where brand = br;
end;
$$ language plpgsql;

select *
from automobiles
where brand = 'BMW';

call UpdatePriceForBrand(20, 'BMW');

-- Рекурсивная хранимая процедура
create or replace procedure CountPeopleBetweenAge(startAge int, endAge int, in count int)
as $$
declare
    num int;
begin
    if startAge > endAge then
        raise notice '%', count;
        return;
    end if;

    select count(*) into num
    from customers
    where age = startAge;
    count := count + num;
    call CountPeopleBetweenAge(startAge + 1, endAge, count);
end;
$$ language plpgsql;

-- Вывод
create or replace procedure CountPeopleBetweenAgePrint(startAge int, endAge int)
as $$
begin
    raise notice 'People between % and % years old: ', startAge, endAge;
    call CountPeopleBetweenAge(startAge, endAge, 0);
end;
$$ language plpgsql;

call CountPeopleBetweenAgePrint(40, 60);


-- Хранимая процедура с курсором
-- Названия моделей, имеющих заданную подстроку
create or replace procedure FindModel(inputText varchar(50))
as $$
declare
	m_name varchar(50);
    myCursor cursor
	for
        select model
		from automobiles
		where model like inputText;
begin
    open myCursor;
    loop
        fetch myCursor
        into m_name;
        exit when not found;
        raise notice 'Model =  %', m_name;
    end loop;
    close myCursor;
end
$$ language plpgsql;

call FindModel('%1%');

-- Хранимая процедура доступа к метаданным
-- Информация о типах полей заданной таблицы
create or replace procedure metaData(tablename varchar(100))
as $$
declare
	c_name varchar(50);
	d_type varchar(50);
    myCursor cursor
	for
        select column_name, data_type
		from information_schema.columns
        where table_name = tablename;
begin
    open myCursor;
    loop
		fetch myCursor
        into c_name, d_type;
		exit when not found;
        raise notice 'column = %; dtype = %', c_name, d_type;
    end loop;
	close myCursor;
end;
$$ language plpgsql;

call metaData('engines');

-- Триггер AFTER
-- Создаем log таблицу
create table upd_info(
    updated_vin varchar(17),
    last_date timestamp,
    last_user text);
drop table upd_info;

-- Создаем функцию для триггера
create or replace function UpdateTrigger()
returns trigger
as $$
begin
	raise notice 'New =  %', new;
    raise notice 'Old =  %', old;
	insert into upd_info(updated_vin, last_date, last_user)
    values(new.vin, current_timestamp, current_user);
	return new;
end
$$ language plpgsql;

-- Создаем триггер
create trigger update_my
after update on automobiles
for each row
execute procedure updateTrigger();


-- Запрос, после которого сработает триггер
update automobiles
set model = 'Vedro'
where model like '%KALINA%';

update automobiles
set model = 'KALINA'
where model like '%Vedro%';

-- Проверка наличия калин
select *
from automobiles
where model like '%KALINA%' or model like 'Vedro';

select *
from upd_info;


-- Тригер INSTEAD OF
-- Сделать поле с инфой об удалении
alter table automobiles add column deleted bool;

-- Создаем представление
create view autoview as
select *
from automobiles;

--Создаем функцию для триггера
create or replace function DeleteAutos()
returns trigger
as $$
begin
    update autoview
    set deleted = true
    where autoview.vin = old.vin;
    return new;
end
$$ language plpgsql;

--Создаем триггер
create trigger deleteAutosTrigger
instead of delete on autoview
for each row
execute procedure DeleteAutos();

--Пытаемся удалить кортеж по условию
delete from autoview
where prod_year = 2003;

select *
from autoview
where prod_year = 2003;

select *
from automobiles
where prod_year = 2003;

-- Задание на защиту
-- Процедура, в которую подается id покупателя и выдается таблица автосалонов, в которых он был и автомобилей, которые там представлены
create or replace procedure GetShowroomsById(custId int)
as $$
declare
	data record;
    myCursor cursor
	for
        select *
        from customers_showrooms c join (select ogrn, full_name, string_agg(au.brand, '; ') as cars
                                         from automobiles au join showrooms s on au.showroom_ogrn = s.ogrn
                                         group by ogrn) tab
        on tab.ogrn = c.showroom_ogrn
        where customer_id = custId;
begin
    open myCursor;
    loop
		fetch myCursor
        into data;
		exit when not found;
        raise notice 'Showroom_name: %.   Cars:  %', data.full_name, data.cars;
    end loop;
	close myCursor;
end;
$$ language plpgsql;



call GetShowroomsById(33);



