# Базы данных. Семинар 6

### Оконные функции
lead и lag

kpp:

|id|type|dttm|
|---|---|---|
|1|1|09:00:00|
|1|2|10:15:00|
|1|1|10:40:00|
|1|2|19:00:00|
|2|1|09:00:00|
|2|2|19:00:00|

```
id - работник
type:
1 - вошел в здание через турникет
2 - вышел в здание через турникет

ps это ескд версионность
```

С помощью lag lead можно получить ескд2 (был на работе с ... по ...)
```sql
select *
from kpp

-- id = 1, dttm = 1:30
-- 1 варик
select type
from kpp
where id = 1 and dttm <= '10:30'
order by dttm desc
limit 1

-- 2 варик
-- explain
select type
from (
     select *,
            row_number() over(partition by id order by dttm desc) rn
     from kpp
     where id = 1 and dttm <= '10:30'
)
where rn = 1

-- 3 варик
select type
from kpp
where kpp.id = 1
      and kpp.dttm = ( select max(dttm)
                       from kpp
                       where dttm <= '10:30') 

-- 4 варик (лучший варик с точки зрения оптимизации)
select type
from (
     select *,
            max(dttm) over(partition by id) m
     from kpp
     where id = 1 and dttm <= '10:30'
)
where dttm = m

-- 5 варик
select id, type, dttm df,
       lead(dttm[, 1, '00:00']) over(partition by id order by dttm)
       - interval '1 second' dt
from kpp

select type
from (
     select id, type, dttm df,
            lead(dttm[, 1, '00:00']) over(partition by id order by dttm)
            - interval '1 second' dt
     from kpp
 ) t
where i = 1 and '10:30' between df and dt
```