-- 1. Выгрузить данные из таблиц в JSON
select row_to_json(a) from automobiles a;
select row_to_json(m) from manufacturers m;
select row_to_json(e) from engines e;
select row_to_json(s) from showrooms s;
select row_to_json(c) from customers c;
select row_to_json(cs) from customers_showrooms cs;

-- Загружаем данные в файл
copy (select row_to_json(a) from automobiles a)
to '/db_data/json_files/automobiles.json';
copy (select row_to_json(m) from manufacturers m)
to '/db_data/json_files/manufacturers.json';
copy (select row_to_json(e) from engines e)
to '/db_data/json_files/engines.json';
copy (select row_to_json(s) from showrooms s)
to '/db_data/json_files/showrooms.json';
copy (select row_to_json(c) from customers c)
to '/db_data/json_files/customers.json';
copy (select row_to_json(cs) from customers_showrooms cs)
to '/db_data/json_files/customers_showrooms.json';



-- 2. Создание таблицы по полученному JSON

-- Создаем таблицу со столбцом типа JSON
drop table if exists json_data;
create table json_data(data json);

-- Копируем данные JSON из файла в созданную таблицу
copy json_data(data)
from '/db_data/json_files/manufacturers.json';

select *
from json_data;

-- Таблица-копия таблицы manufacturers
drop table if exists manufacturers_json;
create table manufacturers_json(
    brand varchar(30) not null primary key,
    country varchar(40) not null,
    found_year int check (found_year between 1000 and 2022),
    founder varchar(50)
);
select *
from manufacturers_json;

-- Заполняем таблицу данными из таблицы с данными JSON
insert into manufacturers_json(brand,
                               country,
                               found_year,
                               founder)
select data->>'brand',
       data->>'country',
       (data->>'found_year')::int,
       data->>'founder'
from json_data;


-- 3. Создать таблицу с атрибутами типа JSON (или добавить к существующей столбец)
alter table automobiles
add column json_data json;

-- Добавляем данные JSON
update automobiles
set json_data = '{"color":"blue", "SteeringWheel":"right", "turbine":"yes"}'
where brand in (select brand
                from manufacturers
                where country = 'Япония');

update automobiles
set json_data = '{"color":"blue", "SteeringWheel":"left", "turbine":"no"}'
where brand in (select brand
                from manufacturers
                where country = 'Германия');

update automobiles
set json_data = '{"color":"White", "SteeringWheel":"left", "turbine":"no"}'
where brand in (select brand
                from manufacturers
                where country = 'Корея');

select *
from automobiles;


-- 4. Выполнить следующие действия:

-- Извлечь XML/JSON фрагмент из XML/JSON документа
-- Извлечь значения конкретных узлов или атрибутов JSON документа
create table temp_table(data json);

copy temp_table
from '/db_data/json_files/customers.json';

select *
from temp_table;

drop table if exists json_test;
create table json_test(
    surname varchar(40),
    first_name varchar(40)
);

    -- Выбираем людей с фамилиями с 'ул' и с именями, начинающимися на А
insert into json_test(surname, first_name)
select data->>'surname', data->>'first_name'
from temp_table
where data->>'surname' like '%ул%';

select *
from json_test;

-- Изменить XML/JSON документ
update json_test
set surname = surname || '-Эдриан'
where first_name like 'А%'

-- Разделить XML/JSON документ на несколько строк по узлам
drop table if exists json_test_2;
create table json_test_2(
    automobile varchar(30),
    info json);

insert into json_test_2 (automobile, info)
values ('Nissan Skyline', '[{"color":"red", "SteeringWheel":"right", "turbine":"yes"}, {"color":"blue", "SteeringWheel":"left", "turbine":"no"}]');

select *
from json_test_2;

select automobile, json_array_elements(info)
from json_test_2;


-- Защита
drop table if exists json_help;
create table json_help(data json);

copy json_help(data)
from '/db_data/json_files/automobiles.json';

select *
from json_help;

select data->>'vin',
       data->>'brand',
       data->>'model',
       (data->>'price')::int,
       (data->>'prod_year')::int,
       data->>'gearbox'
from json_help
where data->>'gearbox' = 'Механическая';

