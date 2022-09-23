# Базы данных. Лекция 4
```
S = {Sno:integer, Sname:string, Status:real, City:string}
P = {Pno:integer, Pname:string, Color:real, Weight:real, City:string}
SP = {Sno:integer, Pno:integer, Qty:integer}
```

1. __Расширение (EXTEND)__

```sql
extend S add 'text' as newA
((extend P add (weight(1000) as new)))[...] rename ...
```

2. __Обобщение (SUMMARIZE)__
```sql
summarize A per B add (<функция>) as atr

summarize SP per SP[Sno]
add sum(Qty) as total
-- {Sno, total}
```

3. __Группировка__
```sql
SP group  {Pno, Qty} as PQ
--{Sno, PQ}
--Pr:={Pno, Qty}
```

4. __Сравнение__  
<реляционное_выражение><сравнение><реляционное_выражение>
- \>  - супермножество 
- \>= - сщбственное супермножество 
- \<  - подмножество 
- \<= - собственное подмножество 
- \=  - равно 
- \<> - не равно 

5. __IS_EMPTY__ (<отношение>)

###  Исчисление кортежей
- **объявление кортежной переменной** ::= RANGE of кор_перем is <список_областей>
- **область** ::= отношение | реляционное_выражение
- **реляционное_выражение** ::= (список_целых_элементов)[where wff]
- **целый_элемент** ::= переменная | переменная атрибут [as имя]
- **wff** ::= условия | NOT у. | AND у. | OR у. | IF у. then wff | EXISTS переменная(wff) | FORA || переменная(wff)
- **условия** ::= (wff) | компоранд отношения копоранд_отн
```sql
range of SPX is SP
range of SX is S
(SX.Sname) where SX.City = 'Смоленск'
(SX) where exists (SPX SX.Sno = SPX.Sno and SPW.Pno = 2)
```