# Базы данных. Семинар 4

**A**

|id|name|
|---|---|
|1|a|
|2|b|
|2|c|
|null|d|
|4|e|
|null|f|
|5|g|

**B**

|id|name|
|---|---|
|1|a|
|1|b|
|2|c|
|null|d|
|null|f|
|5|e|
|6|g|

|A.id|A.name|B.id|B.name|
|---|---|---|---|
|inner||||
|1|a|1|a|
|1|a|1|b|
|2|b|2|c|
|2|c|2|c|
|5|g|5|f|
|left||||
|null|d|null|null|
|4|e|null|null|
|right||||
|null|null|null|d|
|null|null|null|e|
|null|null|6|g|


### Соединение (join)
Делятся на 2 типа:
* Логические
* Физические

#### Логические
* Внутренние
  * inner

    Пример
    ```sql
    select A.*, B.*
    from A inner join B
    on A.id = B.id --предикат
    ```

* Внешние (outer)
  * left join
  * right join
  * full join

  `Fj = Lj + Rj - Ij`





#### Физические
  * Nested Loops Join
    * Преимущества:
      * Любое условие
    * Недостатки:
      * Сложность `O(n * m)`
  * Merge Join
    * Преимущества:
      * Досрочный выход из цикла
      * Cложность `O() < O(n * m)`
    * Недостатки:
      * Необходимость дополнительной сортировка
  * Hash join
    * Преимущества:
      * Быстрее
    * Недостатки:
      * Необходимы дополнительные ресурсы
      * Коллизии
      * Можно применять, только когда условие 'равно'

---
#### Задача
A (id) - 10 строк

B (id) - 20 строк

| |min|max|
|---|---|---|
|Lj|10|200|
|Fl|20|200|
---
#### Задача

**S**

|id|sub|
|---|---|
|1|sub1|
|2|sub2|

**B**

|id|bonus|
|---|---|
|2|bonus1|
|3|bonus2|

Хотим вывести в таком формате

|id|sub|bonus|
|---|---|---|
|1|sub1|null|
|2|sub2|bonus1|
|3|null|bonus2|

```sql
select coalisce(S.id, B.id, 0) as id,
    S.sub, B.bonus
from S full join B
    on S.id = B.id
```

---
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
