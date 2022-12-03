import psycopg2

con = psycopg2.connect(
  database="postgres",
  user="postgres",
  password="postgres",
  host="localhost",
  port="228"
)

print("Successed connection!")



def result_output(result):
  for note in result:
    for var in note:
      print("{:^30}".format(var), end='')
    print()


# Выполнить скалярный запрос
# Список производителей, год основания которых лежит в пределах от 1800 до 1900 года
def task_1():
  print("Список производителей, год основания которых лежит в пределах от 1800 до 1900 года")
  cursor = con.cursor()
  cursor.execute("select * from manufacturers where found_year between 1800 and 1900")
  result = cursor.fetchall()
  result_output(result)


# Выполнить запрос с несколькими соединениями (JOIN)
# Японские автомобили не раньше 2012 года выпуска и стоимостью меньше миллиона руб.
def task_2():
  print("Японские автомобили не раньше 2012 года выпуска и стоимостью меньше миллиона руб.")
  cursor = con.cursor()
  cursor.execute("select au.brand, au.model, au.price, au.prod_year \
                  from automobiles as au join manufacturers as mn on au.brand = mn.brand \
                  where au.prod_year > 2012 \
                  and au.price < 1000000 \
                  and mn.country = 'Япония' \
                  group by au.price, au.brand, au.model, au.prod_year")
  result_output(cursor.fetchall())


# Выполнить запрос с ОТВ(CTE) и оконными функциями
def task_3():
  print("Вывод средних, минимальных и максимальных значений цены по различным группам")
  cursor = con.cursor()
  cursor.execute("select brand, model, price, \
                  avg(price) over (partition by brand) as avg_brand_price, \
                  min(price) over (partition by brand order by model) as min_brand_price, \
                  max(price) over (partition by model) as max_model_price \
                  from automobiles")

  result_output(cursor.fetchall())


# Выполнить запрос к метаданным
# Вывод данных о таблице automobiles
def task_4():
  print("Вывод данных о таблице automobiles")
  cursor = con.cursor()
  cursor.execute("select column_name, data_type \
                  from information_schema.columns \
                  where table_name = 'automobiles'")
  result_output(cursor.fetchall())


# Вызвать скалярную функцию (написанную в третьей лабораторной работе)
# Значение цены с примением указанной скидки
def task_5():
  print("Значение цены с примением указанной скидки")
  cursor = con.cursor()
  cursor.execute("select model, brand, price, PriceSale(price, 25) \
                  from automobiles")
  result_output(cursor.fetchall())


# Вызвать многооператорную или табличную функцию (написанную в третьей лабораторной работе)
# Автомобили заданного бренда или заданного года производства
def task_6():
  print("Автомобили заданного бренда или заданного года производства")
  cursor = con.cursor()
  cursor.execute("select * \
                  from GetAutosByBrandOrProdYear('Nissan', 2000)")
  result_output(cursor.fetchall())


# Вызвать хранимую процедуру (написанную в третьей лабораторной работе)
# Обновление цены на заданный процент у указанного бренда
def task_7():
  print("Обновление цены на заданный процент у указанного бренда")
  cursor = con.cursor()
  cursor.execute("call UpdatePriceForBrand(20, 'BMW')")
  cursor.execute("select * \
                 from automobiles \
                 where brand = 'BMW'")
  result_output(cursor.fetchall())




# Вызвать системную функцию или процедуру
# Имя пользователя в текущем контексте выполнения
def task_8():
  print("Имя пользователя в текущем контексте выполнения")
  cursor = con.cursor()
  cursor.execute("select * from current_user")
  result_output(cursor.fetchall())


# Создать таблицу в базе данных, соответствующую тематике БД
# Создание таблицы скидок по брендам авто
def task_9():
  print("Создание таблицы скидок по брендам авто")
  cursor = con.cursor()
  try:
    cursor.execute("drop table if exists sales;")
    cursor.execute("create table public.sales( \
                    id int generated always as identity primary key, \
                    brand varchar(30) not null, \
                    sale int check (sale between 0 and 100))")
    con.commit()
  except Exception:
    print("Ошибка создания таблицы")
    con.rollback()


# Выполнить вставку данных в созданную таблицу с использованием инструкции INSERT или COPY
# Заполнение таблицы sales
def task_10():
  try:
    print("Вставить данные в таблицу sales")
    cursor = con.cursor()
    cursor.execute("insert into sales(brand, sale) values \
                  ('BMW', 20), \
                  ('Mercedes-Benz', 5), \
                  ('LADA', 100), \
                  ('Lamborghini', 1); \
                  select * from sales;")
    result_output(cursor.fetchall())
    con.commit()
  except:
    con.rollback()


def menu():
  print("------------------MENU------------------")
  print("1. Выполнить скалярный запрос")
  print("2. Выполнить запрос с несколькими соединениями (JOIN)")
  print("3. Выполнить запрос с ОТВ(CTE) и оконными функциями")
  print("4. Выполнить запрос к метаданным")
  print("5. Вызвать скалярную функцию (написанную в третьей лабораторной работе)")
  print("6. Вызвать многооператорную или табличную функцию (написанную в третьей лабораторной работе)")
  print("7. Вызвать хранимую процедуру (написанную в третьей лабораторной работе)")
  print("8. Вызвать системную функцию или процедуру")
  print("9. Создать таблицу в базе данных, соответствующую тематике БД")
  print("10. Выполнить вставку данных в созданную таблицу с использованием инструкции INSERT или COPY")
  print("0. Выход")
  print("----------------------------------------")


def input_choice():
  choice = -1
  while choice < 0 or choice > 10:
    try:
      choice = int(input("> "))
      if choice < 0 or choice > 10:
        print("Введите число от 0 до 10")
    except Exception:
      print("Введите число от 0 до 10")
  return choice


while True:
  menu()
  choice = input_choice()
  if  choice == 1:
    task_1()
  elif choice == 2:
    task_2()
  elif choice == 3:
    task_3()
  elif choice == 4:
    task_4()
  elif choice == 5:
    task_5()
  elif choice == 6:
    task_6()
  elif choice == 7:
    task_7()
  elif choice == 8:
    task_8()
  elif choice == 9:
    task_9()
  elif choice == 10:
    task_9()
    task_10()
  else:
    break