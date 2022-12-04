from py_linq import *

class Automobile():
    vin = str()
    brand = str()
    model = str()
    price = int()
    prod_year = int()
    transmission = str()
    gearbox = str()
    showroom_ogrn = str()
    anc_auto = str()

    def __init__(self, vin, brand, model, price, prod_year, transmission, gearbox, showroom_ogrn, anc_auto):
        self.vin = vin
        self.brand = brand
        self.model = model
        self.price = price
        self.prod_year = prod_year
        self.transmission = transmission
        self.gearbox = gearbox
        self.showroom_ogrn = showroom_ogrn
        self.anc_auto = anc_auto

    def get(self):
        return {'vin': self.vin, 'brand': self.brand, 'model': self.model,
                'price': self.price, 'prod_year': self.prod_year,
                'transmission': self.transmission, 'gearbox': self.gearbox,
                'showroom_ogrn': self.showroom_ogrn, 'anc_auto': self.anc_auto}


def get_automobiles_array(filename):
    file = open(filename, 'r')
    automobiles = []
    for line in file:
        elems = line.split(';')
        automobiles.append(Automobile(elems[0], elems[1], elems[2], int(elems[3]), int(elems[4]), elems[5],
                                      elems[6], elems[7], elems[8]).get())
    return automobiles


class Engine():
    vin = str()
    power = int()
    cylinders = int()
    capacity = float()
    consumption = float()

    def __init__(self, vin, power, cylinders, capacity, consumption):
        self.vin = vin
        self.power = power
        self.cylinders = cylinders
        self.capacity = capacity
        self.consumption = consumption

    def get(self):
        return {'vin': self.vin, 'power': self.power, 'cylinders': self.cylinders,
                'capacity': self.capacity, 'consumption': self.consumption}


def get_engines_array(filename):
    file = open(filename, 'r')
    engines = []
    for line in file:
        elems = line.split(';')
        engines.append(Engine(elems[0], int(elems[1]), int(elems[2]), float(elems[3]), float(elems[4])).get())
    return engines




def request_01(automobiles):
    return automobiles.select(lambda x: {x['model']})


def request_02(automobiles):
    return automobiles.where(lambda x: x['prod_year'] > 2012).select(lambda x: {x['brand'], x['model'], x['prod_year']})


def request_03(automobiles):
    return automobiles.group_by(key_names=['brand'], key=lambda x: x['brand']).select(lambda g: { 'key': g.key.brand, 'count': g.count() })


def request_04(automobiles, engines):
    return automobiles.join(engines, lambda a: a['vin'], lambda e: e['vin'], lambda result: result)


def request_05(engines):
    return engines.where(lambda x: x['consumption'] > 8).select(lambda x: x['power']).min()


def print_res(res, msg):
    print(msg)
    count = 8
    for i in range(count):
        print(res[i])
    print()


def task_1():
    automobiles = Enumerable(get_automobiles_array("D:\\Users\Alexey\Documents\\University\semester_5\db\lab_01\csv_files\\autos.csv"))
    engines = Enumerable(get_engines_array("D:\\Users\Alexey\Documents\\University\semester_5\db\lab_01\csv_files\\engines.csv"))

    print_res(request_01(automobiles), "1. Вывод нескольких моделей авто")
    print_res(request_02(automobiles), "2. Автомобили, выпущенные после 2012")
    print_res(request_03(automobiles), "3. Количество авто каждой марки")
    print_res(request_04(automobiles, engines), "4. Join таблицы авто и двигателей")
    print("5. Наименьшая мощность двигателя, у которого расход больше 8\n", request_05(engines))
