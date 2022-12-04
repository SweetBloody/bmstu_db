create extension plpython3u;

-- 1. Определяемая пользователем скалярная функция CLR
-- Разбиение автомобилей по классам в зависимости от привода
drop function auto_class;

create or replace function auto_class(transmission text)
returns varchar as
$$
    if transmission == 'Передний':
        return 'Дефолт'
    elif transmission == 'Полный':
        return "Внедорожник"
    elif transmission == 'Задний':
        return 'Дрифт-корч'
$$ language plpython3u;

select model, brand, transmission, auto_class(transmission)
from automobiles;





-- 2. Пользовательская агрегатная функция CLR
-- Получить среднюю мощность машин заданного бренда
drop function avg_power_brand;

create or replace function avg_power_brand(name text)
returns float as
$$
	plan = plpy.prepare("select power from automobiles a join engines e on a.vin = e.vin where a.brand = $1", ['text'])
	result = plpy.execute(plan, [name])
	count = 0
	avg_power = 0
	print(result)
	if result is not None:
		for i in result:
			count += 1
			avg_power += i['power']
	return avg_power / count
$$ language plpython3u;

select avg_power_brand('Nissan');




-- 3. Определяемая пользователем табличная функция CLR
-- Автомобили с заданной мощностью
drop function autos_with_power;

create or replace function autos_with_power(num int)
returns table (brand varchar(30), model varchar(40), power int, capacity numeric(3, 1)) as
$$
	plan = plpy.prepare("select brand, model, power, capacity \
                        from automobiles a join engines e on a.vin = e.vin \
                        where e.power = $1", ['int'])
	result = plpy.execute(plan, [num])
	table = list()
	if result is not None:
		for i in result:
			table.append(i)
	return table
$$ language plpython3u;

select * from autos_with_power(243);




-- 4. Хранимая процедура CLR
-- Обновление цены на заданный процент у указанного бренда
drop procedure update_price_for_brand;

create or replace procedure update_price_for_brand(proc int, br text) as
$$
    plan = plpy.prepare("update automobiles \
                        set price = price * (1 + $1::real / 100) \
                        where brand = $2;", ["int", "text"])
    plpy.execute(plan, [proc, br])
$$ language plpython3u;

select *
from automobiles
where brand = 'BMW';

call update_price_for_brand(20, 'BMW');




-- 5. Триггер CLR
-- Пишем в консоль об изменении
drop function update_trigger_CLR cascade;

create or replace function update_trigger_CLR()
returns trigger
as $$
    plpy.notice("--------------------------------")
    plpy.notice("New: {}".format(TD["new"]))
    plpy.notice("Old: {}".format(TD["old"]))
    plpy.notice("--------------------------------")
$$ language plpython3u;

-- Создаем триггер
create trigger update_CLR
after update on automobiles
for each row
execute procedure update_trigger_CLR();

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





-- 6. Определяемый пользователем тип данных CLR
drop type info_showrooms cascade ;

create type info_showrooms as
(
    ogrn varchar(13),
    full_name varchar(50),
    first_name varchar(15),
    surname varchar(15)
);

-- Инфа об автосалонах дилерах заданного бренда
create or replace function showroom_info(br text)
returns setof info_showrooms as
$$
	plan = plpy.prepare("select ogrn, full_name, first_name, surname \
						from showrooms sh join customers c on sh.owner_id = c.id \
						where brand = $1;", ["text"])
	res = plpy.execute(plan, [br])
	if res is not None:
		return res
$$ language plpython3u;

select * from showroom_info('Dumpen');

-- Защита

drop table tables_info;
create table tables_info(
    table_name text,
    strings_count int
);

insert into tables_info
values ('automobiles', 1000);

drop function update_tables_clr cascade;

create or replace function update_tables_clr(table_name text)
returns trigger
as $$
    plan = plpy.prepare("select * from $1", ["text"])
    table = list(plpy.execute(plan, [table_name]))
    plan = plpy.prepare("update tables_info \
                        set strings_count = $1 \
                        where table_name = '$2'", ["int", "text"])
    plpy.execute(plan, [len(table), table_name])
$$ language plpython3u;

create trigger insert_auto_trig
after insert on automobiles
for each row
execute procedure update_tables_clr('automobiles');

insert into automobiles
values ('CX9EZAA45FSGH01S8', 'Nissan', 'Skyline', 1200000, 2002, 'Полный', 'Автоматическая', 5171948384427, 'SGPNBH3Z5R9SVNHJ1');

insert into automobiles
values ('CX9EZGHR8K9WZ01S8', 'Toyota', 'Rav', 1200000, 2002, 'Полный', 'Автоматическая', 5171948384427, 'SGPNBH3Z5R9SVNHJ1');

select *
from tables_info;