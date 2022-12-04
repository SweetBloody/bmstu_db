from peewee import *

db = PostgresqlDatabase(
    database="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="228"
)


class BaseModel(Model):
    class Meta:
        database = db


class Automobiles(BaseModel):
    vin = PrimaryKeyField(column_name='vin')
    brand = CharField(column_name='brand')
    model = CharField(column_name='model')
    price = IntegerField(column_name='price')
    prod_year = IntegerField(column_name='prod_year')
    transmission = CharField(column_name='transmission')
    gearbox = CharField(column_name='gearbox')
    showroom_ogrn = CharField(column_name='showroom_ogrn')
    anc_auto = CharField(column_name='anc_auto')

    class Meta:
        table_name = 'automobiles'


class Engines(BaseModel):
    vin = PrimaryKeyField(column_name='vin')
    power = IntegerField(column_name='power')
    cylinders = IntegerField(column_name='cylinders')
    capacity = FloatField(column_name='capacity')
    consumption = FloatField(column_name='consumption')

    class Meta:
        table_name = 'engines'


class Manufacturers(BaseModel):
    brand = PrimaryKeyField(column_name='brand')
    country = CharField(column_name='country')
    found_year = IntegerField(column_name='found_year')
    founder = CharField(column_name='founder')

    class Meta:
        table_name = 'manufacturers'


def request_01():
    result = Automobiles.select(Automobiles.brand, Automobiles.model, Automobiles.prod_year).\
        where(Automobiles.prod_year > 2002)
    for row in result.namedtuples():
        print("{:^30}{:^30}{:^30}".format(row.brand, row.model, row.prod_year))


def request_02():
    result = Automobiles.select(Automobiles.vin, Automobiles.brand, Automobiles.model, Engines.power).\
        join(Engines, on=(Automobiles.vin == Engines.vin)).\
        where(Engines.power > 200)
    for row in result.namedtuples():
        print("{:^30}{:^30}{:^30}{:^30}".format(row.vin, row.brand, row.model, row.power))


def print_automobiles():
    print("\nAutomobiles:")
    result = Automobiles.select(Automobiles.vin, Automobiles.brand, Automobiles.model, Automobiles.prod_year, Automobiles.price)
    for row in result.namedtuples():
        print("{:^30}{:^30}{:^30}{:^30}{:^30}".format(row.vin, row.brand, row.model, row.prod_year, row.price))


def print_manufacturers(brand):
    print("\nManufacturers:")
    result = Manufacturers.select().where(Manufacturers.brand == brand)
    for row in result.namedtuples():
        print("{:^30}{:^30}{:^30}{:^30}".format(row.brand, row.country, row.found_year, row.founder))


def adding(vin, brand, model, price, prod_year, transmission, gearbox, showroom_ogrn, anc_auto):
    Automobiles.create(vin=vin, brand=brand, model=model, price=price, prod_year=prod_year, transmission=transmission,
                       gearbox=gearbox, showroom_ogrn=showroom_ogrn, anc_auto=anc_auto)
    print("Added!")


def updating(brand, sale):
    try:
        automobiles = Automobiles.select().where(Automobiles.brand == brand)
        for auto in automobiles:
            auto.price = auto.price * (100 - sale) // 100
            auto.save()
        print("Updated!")
    except Exception as exc:
        print(exc)


def deleting(brand):
    try:
        manufacturer = Manufacturers.get(brand=brand)
        manufacturer.delete_instance()
        print("Deleted!")
    except Exception as exc:
        print(exc)


def request_03():
    print("-- Добавление в таблицу")
    vin = input("VIN-номер:")
    brand = input("Марка авто: ")
    model = input("Модель авто: ")
    price = int(input("Цена: "))
    prod_year = int(input("Год производства: "))
    transmission = "Полный"
    gearbox = "Механическая"
    showroom_ogrn = "1067812900792"
    anc_auto = "A20NCEDG8HAPA2X1C"
    adding(vin, brand, model, price, prod_year, transmission, gearbox, showroom_ogrn, anc_auto)
    print_automobiles()

    print("-- Обновление таблицы")
    brand = input("Марка авто: ")
    sale = int(input("Скидка (от 0 до 100): "))
    while sale < 0 or sale > 100:
        sale = int(input("Скидка (от 0 до 100): "))
    updating(brand, sale)
    print_automobiles()

    print("-- Удаление из таблицы")
    brand = "Rest"
    print_manufacturers(brand)
    deleting(brand)
    print_manufacturers(brand)


def request_04():
    cursor = db.cursor()
    print("Названия моделей, имеющих заданную подстроку (цифру 1)")
    cursor.execute("call UpdatePriceForBrand(20, 'Toyota')")
    print_automobiles()


def task_3():
    print("1. Все автомобили от 2002 года выпуска:")
    request_01()

    print("2. Автомобили с мощностью больше 200:")
    request_02()

    print("3. 3 запроса")
    request_03()

    print("4. Получение доступа к данным с помоью хранимой процедуры")
    request_04()


