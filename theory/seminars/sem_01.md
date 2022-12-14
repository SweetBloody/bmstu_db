# Базы данных. Семинар 1

> Отношение - это по сути таблица.

| $a_1$ | $a_2$ |  ...  | $a_n$ |  ...  |
|-------|-------|-------|-------|-------|
|  ...  |  ...  |  ...  |  ...  |  ...  |

Строка $a_1$, $a_2$, ..., $a_n$ - заголовок.  
Столбец $a_1$, $a_2$ и т.д. - атрибуты.  
Отдельные строки - кортежи.  
Тело - множество кортежей значений атрибутов.  

Множество:
- Уникальность
- Неупорядоченность

---
### SQL
SQL - это стандарт. В него входят 3 языка:
* DDL - data defenition language (язык обработки объектов)
    - создать объект БД - `create`
    - удалить - `drop`
    - изменить - `alter`
* DML - data manipulation language (язык обработки данных)
    - вставить - `insert`
    - удалить - `delete`  
```delete блокирует только удаляемый кусок```
    - изменить - `update`
    - почитать - `select`
    - удалить все - `truncate`  
```truncate блокирует всю таблицу```
* DCL - data control language (язык доступа к объекту)
    - выдать права - `grant`
    - забрать - `revoke`
    - запретить - `deny`

Как хранить данные:
- Таблица - `table`
- Временная таблица - `temp table`  
```обычно одна транзакция - это она сессия```
- Табличная переменная
- Представление - `view`
- Индексированное представление

Объекты БД:
- Table
- View
- Пользователь
- БД
