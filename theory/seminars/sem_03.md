# Базы данных. Семинар 3

### Корпуса
name|Add|pX|pY|fl
---|---|---|---|---|
УЛК|Рубцовская наб., 8|55.771|37.69|14
ГУК|2-я Бауманская, 5|55.765|37.68|11
СМ|Госпитальный переулок, 10|55.769|37.69|14

SP  

Fid|Kid
---|---|
ИУ|УЛК
ИУ|ГУК|
СМ|СМ|

### Select
| |No|В каком порядке выполняет СУБД
---|---|---|
Select|1|5|
from|2|1 (1.1)|
where|3|2 (1.2)|
group by|4|3|
having|5|4|
order by|6|6|

### Запросы
> В select должны быть только скаляры (все кроме таблиц)
1) **SELECT**  
Общий вид запроса: `select * from table_name`
   ```
   * select 1 + 1 [from dual] (dual - таблица для Oracle из одной ячейки с названием dummy)
   * select now() (текущее время СУБД)
   ```
   ```sql
   select [t.]name AS "Имя корпуса", px, py AS y 
   from table_name AS t
   ```
2) **WHERE**  
   where <предикат>  
Предикаты: 
   * Пр. сравнения: `>, >=, <, <=, =, <>, !=`
   * Пр. `between`
   * Пр. `is [not] NULL` (NULL != NUL, 1 + NULL = NULL, sum(1, NULL) = 1)
   * Пр. `like` - % (строка символов) и _ (ровно один символ)
   * Пр. `in` (позволяет проверить атрибут на вхождение в множество)
   * Пр. `exists` (Возвращает либо true, либо false)
```sql
select * from "Корпуса" AS t
where fl > 13 and fl <= 15
where fl between 13 and 15
where py is NULL
where Add like '%2%'
where fl in (11, 12, 13, 14)
where (px, py) in ((55, 37), ...)

select * from SP
where Kid in (
   select name
   from "Корпуса"
   where fl > 13)

select * from SP
where exists (
   select *
   from "Корпуса"
   where fl > 13)
-- В данном случае запрос вернет всю таблицу SP, так как 'where fl > 13' вернет true,
-- а значит exists тоже вернет true

-- Чтобы исправить - используем кореллированный запрос (связь двух таблиц)
select * from SP as S
where exists (
   select *
   from "Корпуса"
   where fl > 13 and 
        S.Kid = name)
```

3) **GROUP**  
```sql
select fl, count(*)
from "Корпуса"
group by fl
```

4) **HAVING**  
Группы, в котрорых количество зданий больше двух
```sql
select fl, count(*)
from "Корпуса"
group by fl
having count(*) >= 2 / select ...

select fl, count(*) as cnt
from "Корпуса"
group by fl
having cnt >= 2  
-- работать не будет, потому что select выполняется последним, 
-- а именно там мы задаем новое имя, но переименование все равно используется для 'order by'

order by cnt
```
