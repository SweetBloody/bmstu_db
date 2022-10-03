# Базы данных. Семинар 5

#### Задача

|id|p_name|p_value|
|---|---|---|
|1|name|Yulia|
|1|gender|f|
|2|name|Ivan|

Хотим получить такую таблицу

|id|name|gender|
|---|---|---|
|1|Yulia|f|
|2|Ivan|null|

```sql
select t1.id, t1.p_value as name, t2.p_value as gender
from t1 join t2 on t1.id = t2.id
where t1.p_name = 'name'
    and t2.p_name = 'gender'
```

#### Как решить без join?

Если мы заранее знаем атрибуты, то можем сделать так

```sql
select id
    case when p_name = 'value'
        then p_value
        else null end as name
    case when p_name = 'gender'
        then p_value
        else null end as gender
```

Получим таблицу вида

|id|name|gender|
|---|---|---|
|1|Yulia|null|
|1|null|f|
|2|Ivan|null|

Теперь группируем

```sql
select id
    max(case when p_name = 'value'
        then p_value
        else null end) as name
    max(case when p_name = 'gender'
        then p_value
        else null end) as gender
from t
group by id
```

### Обобщенное табличное выражение
> Обобщенное табличное выражение - выражение, которое выполняется перед запросом (предрасчет)

Пример:

```sql
with n (id, name) as (
    select id, p_value
    from t
    where p_name = 'name'
),
g (id, gender) as (
    select id, p_value
    from t
    where p_name = 'gender'
)

-- далее основной запрос
select id, name, gender
from n join g in n.id = g.id
```

Как только выполнился нижний SELECT, таблицы n и g исчезают

Пример:

Empl

|id|name|m_id|
|---|---|---|
|1|Илья|null|
|2|Иван|4|
|3|Алексей|1|
|4|Святополк|1|
|5|Шехеризада|3|
|6|Хан-Батый|3|

```sql
with [recursive] otv_empl (id, name, m_id, level) as (
-- Якорь----
    select id, name, m_id, 0 as level
    from empl,
    where m_id is null
-- -----
    union all
-- шаг рекурсии
    select e.id, e.name, e.m_id, otv.level + 1
    from empl e inner join otv_empl otv
        on e.m_id = otv.id
-- -----
    )
    select *
    from otv_empl
```

|id|name|m_id|level
|---|---|---|---
|1| |null|0
|3| |1|1
|4| |1|1
|2| |4|2
|5| |3|3
|6| |3|2

1 шаг - 2 и 3 строку мы соединяем с табл empl (рекурсия)

2 шаг - 4 и 5 строка

3 шаг - пустой набор

Как только получили пустой набор строк - завершаем рекурсию

### Оконные функции
`Считаем все на свете в одном запрос`

Выполняет группировки без физической группировки данных.

```
функция(<параметры>) over (partition by <атрибуты>
                            order by <атрибуты>)
``` 


Виды:
- ранжирующие (как то индексируют значения) 
  - `row_number`
  - `rank`
- агрегатные
  - `min`
  - `max`
  - `sum`
  - `avg`
  - `count` (очень редко)
- функции доступа
  - `lag`
  - `lead`

---

Пример:

name|Add|pX|pY|fl
---|---|---|---|---|
УЛК| |55|35|14
ГУК| |54|53|11
СМ| |56|58|14
СК| |54|54|5
Э| |52|53|5
Общага| |56|51|5

```sql
select *
    row_number() over (order by pX) as r1,
    row_number() over (partition by f order by pY) as r2
from t

select *
    max(pY) over (order by pX) as m1,
    max(pY) over (partition by f order by pX) as m2
    max(pY) over (partition by f) as m3
from t

-- lead(name, step=1, default=0)
select *
    lag(name) over (partition by f oder by pX desc) as l1,
    lead(name, 1, '0') over (partition by f oder by pX desc) as l2
from t
```

Получим

name|Add|pX|pY|fl|r1|r2|m1|m2|m3|l1|l2
---|---|---|---|---|---|---|---|---|---|---|---
УЛК| |55|35|14|4|1|55|55|58|СМ|0
ГУК| |54|53|11|2/3|1|53|53|53|null|0
СМ| |56|58|14|5/6|2|58|58|58|null|УЛК
СК| |54|54|5|3/2|3|54|54|54|Общага|Э
Э| |52|53|5|1|2|53|53|54|СК|0
Общага| |56|51|5|6/5|1|58|54|54|null|СК

В случае m2: агрегатная функция имеет накопительный эффект (она выбирает значение из просмотренных строк)