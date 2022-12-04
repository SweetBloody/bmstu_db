import json
import psycopg2
from task_1 import Automobile


def get_json_automobiles(con):
    cursor = con.cursor()
    cursor.execute("copy (select row_to_json(a) from automobiles a) \
                    to '/db_data/json_files/automobiles.json';")
    print("Создание JSON для таблицы automobiles - success!")
    cursor.close()


def data_output(data, keys):
    for key in keys:
        print("{:^30}".format(str(data[key])), end='')
    print()


def read_json(filename):
    file = open(filename, 'r')
    for line in file:
        data = json.loads(line)
        keys = data.keys()
        data_output(data, keys)
    file.close()


def update_json(filename, brand, sale):
    file = open(filename, 'r')
    data = list()
    for line in file:
        data.append(json.loads(line))
    keys = data[0].keys()
    for elem in data:
        if elem['brand'] == brand:
            data_output(elem, keys)
            elem['price'] = elem['price'] * (100 - sale) // 100
            data_output(elem, keys)
    file.close()
    file = open(filename, 'w')
    for elem in data:
        file.write(json.dumps(elem, ensure_ascii=False) + '\n')
    file.close()


def insert_into_json(filename, data):
    file = open(filename, 'a')
    file.write(json.dumps(data, ensure_ascii=False) + '\n')
    file.close()


def task_2():
    con = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port="228"
    )

    get_json_automobiles(con)
    filename = "D:\\Users\Alexey\Documents\\University\semester_5\db\lab_01\json_files\\automobiles.json"

    print("1. Чтение файла JSON")
    read_json(filename)

    print("2. Обновление JSON документ (установка скидки для автомобилей определенной марки)")
    brand = input("Марка авто: ")
    sale = int(input("Скидка (от 0 до 100): "))
    while sale < 0 or sale > 100:
        sale = int(input("Скидка (от 0 до 100): "))
    update_json(filename, brand, sale)

    print("3. Добавление в JSON документ")
    vin = input("VIN-номер:")
    brand = input("Марка авто: ")
    model = input("Модель авто: ")
    price = int(input("Цена: "))
    prod_year = int(input("Год производства: "))
    transmission = "Полный"
    gearbox = "Механическая"
    showroom_ogrn = "1067812900792"
    anc_auto = "A20NCEDG8HAPA2X1C"
    insert_into_json(filename,
                     Automobile(vin, brand, model, price, prod_year, transmission, gearbox, showroom_ogrn, anc_auto).get())
    read_json(filename)
    con.close()


