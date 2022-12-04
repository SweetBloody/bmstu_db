-- 1. Инструкция SELECT, использующая предикат сравнения
-- Японские автомобили не раньше 2012 года выпуска и стоимостью меньше миллиона руб.
select au.brand, au.model, au.price, au.prod_year
from automobiles as au join manufacturers as mn on au.brand = mn.brand
where au.prod_year > 2012
    and au.price < 1000000
    and mn.country = 'Япония'
group by au.price, au.brand, au.model, au.prod_year;

-- 2. Инструкция SELECT, использующая предикат BETWEEN.
-- Список производителей, год основания которых лежит в пределах от 1800 до 1900 года
select *
from manufacturers
where found_year between 1800 and 1900;

-- 3. Инструкция SELECT, использующая предикат LIKE.
-- Список производителей из стран, оканчивающихся на 'лия'
select *
from manufacturers
where country like '%лия%';

-- 4. Инструкция SELECT, использующая предикат IN с вложенным подзапросом.
-- Список двигателей автомобилей с полным приводом, мощность которых больше 175 л с
select vin, power, capacity, consumption
from engines
where vin in (select vin
        from automobiles
        where transmission = 'Полный')
    and power > 175;

-- 5. Инструкция SELECT, использующая предикат EXISTS с вложенным подзапросом.
-- Салоны-представители Nissan
select a.ogrn, a.full_name, a.address
from showrooms a
where exists (select *
        from showrooms
        where showrooms.full_name like '%A%')
    and brand = 'Nissan';

-- 6. Инструкция SELECT, использующая предикат сравнения с квантором.
-- Производители, основанные раньше всех российских производителей
select brand, found_year, country
from manufacturers
where found_year < all(select found_year
        from manufacturers
        where country = 'Россия');


-- 7. Инструкция SELECT, использующая агрегатные функции в выражениях столбцов.
-- Средний расход по маркам автомобилей
select brand, avg(consumption) as avg_consumption
from automobiles as au join engines as en on au.vin = en.vin
group by brand;


-- 8. Инструкция SELECT, использующая скалярные подзапросы в выражениях столбцов.
-- Для сравнения со средней ценой авто после 2020 года
select brand, model, prod_year, price,
       (select avg(price)
        from automobiles
        where prod_year > 2020) as avg_price
from automobiles;


-- 9. Инструкция SELECT, использующая простое выражение CASE.
-- Определение класса авто в зависимости от привода
select brand, model, transmission,
       case transmission
            when 'Передний' then 'Дефолт'
            when 'Полный' then 'Внедорожник'
            when 'Задний' then 'Дрифт-корч'
        end as Class
from automobiles;

-- 10. Инструкция SELECT, использующая поисковое выражение CASE.
-- Определение класса авто в зависимости от мощности
select brand, model, power,
       case
            when power < 100 then 'Ведро'
            when power between 100 and 200 then 'Семейный'
            when power > 200 then 'Спорткар'
        end as Class
from automobiles as au join engines as en on au.vin = en.vin;

-- 11. Создание новой временной локальной таблицы из результирующего набора данных инструкции SELECT.
-- Получить таблицу с названием салона и фио владельца
create temp table if not exists showroom_owners as
select sh.full_name, cu.first_name, cu.surname, cu.otch
from showrooms as sh join customers as cu on sh.owner_id = cu.id;

select *
from showroom_owners;

-- 12. Инструкция SELECT, использующая вложенные коррелированные подзапросы в качестве производных таблиц в предложении FROM.
-- Список моделей, которые представлены только в одном салоне
select *
from automobiles au1
where au1.model not in (
    select au2.model
    from automobiles au2
    where au1.showroom_ogrn <> au2.showroom_ogrn
    );


-- 13. Инструкция SELECT, использующая вложенные подзапросы с уровнем вложенности 3.
select vin, power
from engines
where vin in (select vin
    from automobiles
    where brand in (select brand
        from manufacturers
        where country = 'Италия'));

-- 14. Инструкция SELECT, консолидирующая данные с помощью предложения GROUP BY, но без предложения HAVING.
-- Минимальная и максимальная мощность каждой модели
select au.brand, au.model, min(en.power) as min_power, max(en.power) as max_power
from automobiles as au join engines as en on au.vin = en.vin
group by au.brand, au.model;

-- 15. Инструкция SELECT, консолидирующая данные с помощью предложения GROUP BY и предложения HAVING.
-- Модели авто со средней ценой выше, чем средняя цена по всем авто
select model, avg(price) as avg_price
from automobiles
group by model
having avg(price) > (select avg(price)
    from automobiles);

-- 16. Однострочная инструкция INSERT, выполняющая вставку в таблицу одной строки значений.
insert into manufacturers(brand, country, found_year, founder)
values ('Red Bull', 'Венгрия', 1967, 'Max Ferstappen');

-- 17. Многострочная инструкция INSERT, выполняющая вставку в таблицу результирующего набора данных вложенного подзапроса.
insert into customers(surname, first_name, otch, age, sex)
select (select country
    from manufacturers
    where found_year >= (select max(found_year)
        from manufacturers)
    limit 1),
       brand, 'Моделевич', 77, 'мужской'
from automobiles
where prod_year > 2010;

-- 18. Простая инструкция UPDATE
-- Увеличение стоимости авто с АКПП на 10%
update automobiles
set price = 100
where prod_year = 2022
returning *;

-- 19. Инструкция UPDATE со скалярным подзапросом в предложении SET.
-- Для всех 4-цилиндровых двигателей заменить на максимальную мощность среди 4-цилиндровых двигателей
update engines
set power = (select max(power)
             from engines
             where cylinders = 4)
where cylinders = 4
returning *;

-- 20. Простая инструкция DELETE.
delete from manufacturers
where country = 'Палау';

-- 21. Инструкция DELETE с вложенным коррелированным подзапросом в предложении WHERE.
-- Удаление всех Павлов, которые не являются владельцами автосалонов
delete from customers
where first_name in (select brand
                from manufacturers
                where found_year > 1900)
returning *;

-- 22. Инструкция SELECT, использующая простое обобщенное табличное выражение
-- Вывод брендов, у которых представлено автомобилей больше среднего по всем брендам
with num_brands (brand, number) as (
    select brand, count(*)
    from automobiles
    group by brand
)
select *
from num_brands
where number > (select avg(number)
                from num_brands);

-- 23. Инструкция SELECT, использующая рекурсивное обобщенное табличное выражение.
with recursive auto_anc (vin, brand, model, distance, lvl) as (
-- Якорь----
    select vin, brand, model, anc_auto, 0 as lvl
    from automobiles
    where anc_auto is null
-- -----
    union all
-- шаг рекурсии
    select au.vin, au.brand, au.model, au.anc_auto, anc.lvl + 1
    from automobiles au inner join auto_anc anc on au.anc_auto = anc.vin
-- -----
    )
    select *
    from auto_anc;


-- 24. Оконные функции. Использование конструкций MIN/MAX/AVG OVER()
select brand, model, price,
 avg(price) over (partition by brand) as avg_brand_price,
 min(price) over (partition by brand order by model) as min_brand_price,
 max(price) over (partition by model) as max_model_price
from automobiles;

-- 25. Оконные фнкции для устранения дублей
-- Дублирование мужчин возрастом более 50 лет
insert into customers (surname, first_name, otch, age, sex)
select surname, first_name, otch, age, sex
from customers
where age > 50 and sex = 'мужской';

-- Удаление дублей
with double_cust (id, surname, first_name, otch, age, sex, r_n) as (
    select *,
    row_number() over (partition by surname, first_name, otch, age, sex order by id) as r_n
    from customers)


delete from customers
where id in (select id
             from double_cust
             where double_cust.r_n != 1)
    and id > 3000;

-- 26. Доп задание
-- Получить список брендов и салонов, в которых эти бренды предствлены
create temp table if not exists tempic as
select br.brand, sh.full_name
from (automobiles au join manufacturers br on au.brand = br.brand) join showrooms sh on showroom_ogrn = sh.ogrn;

select brand, string_agg(full_name, '; ')
from tempic
group by brand;

select full_name, string_agg(brand, '; ')
from tempic
group by full_name;


select *
from automobiles


