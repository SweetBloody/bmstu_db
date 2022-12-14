# Базы данных. Семинар 9

### Оптимизация запросов. План запросов
Рассматривать будем на примере PostgreSQL 

Любой запрос проходит 5 стадий:
* прикладная программа устанавливает подключение к PostgreSQL
* на этапе разбора запроса сервер выполняет синтаксическую проверку запроса, переданного прикладной программой и создает дерево запроса 
* система правил принимает дерево запроса, созданное на стадии разбора, и ищет в системных каталогах правила для применения к этому дереву 
* планировщик/оптимизатор принимает дерево запроса (возможно, переписанное) и создает план запроса, который будет передан исполнителю. Он выбирает план, сначала рассматривая все возмоджные варианты получения одного и того же результата 
* исполнитель рекурсивно проходит во дереву влана и получает строки тем способом, который указан в плане 

#### Дерево разбора

Дерево разбора состоит из узлов двух типов:
* Атомы - лексиеские элементы следующих типов:
  * ключевые слова 
  * имена атрибутов или отношений 
  * константы 
  * скобки 
  * операторы (например, + или >)
* Синтаксические категории - имена семейств, представляющих часть запроса. Заключаются в угловые скобки: \<SFW>, \<Condition>


Чтобы добавить join в грамматику
```
<SWF> ::= select <setlist> from fromcondition where condition
fromcondition ::= fromcondition join relation on condition
fromcondition ::= relation, fromcondition
fromcondition ::= relation
relation ::= query
````