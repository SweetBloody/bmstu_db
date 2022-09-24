# http://www.motorpage.ru
from random import randint, choice
from faker import Faker
from faker_vehicle import VehicleProvider


def generate_vin():
    symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    vin = ""
    for i in range(17):
        ind = randint(0, len(symbols) - 1)
        vin += symbols[ind]
    return vin


def check_unique_vin(auto_list, vin):
    for i in range(len(auto_list)):
        if vin == auto_list[i][0]:
            return 1
    return 0


def generate_autos(auto, number, showroom_list):
    gearbox_list = ['Автоматическая', 'Механическая']
    transmission_list = ['Передний', 'Задний', 'Полный']
    keys = list(auto.keys())
    keys_len = len(keys)
    auto_list = []
    for i in range(number):
        key_ind = randint(0, keys_len - 1)
        model = keys[key_ind]
        models_len = len(auto[model])
        key_model = randint(0, models_len - 1)
        year = randint(auto[model][key_model][1], auto[model][key_model][2])
        vin = generate_vin()
        while check_unique_vin(auto_list, vin) == 1:
            vin = generate_vin()
        price = randint(500000, 10500000)
        transmission = choice(transmission_list)
        gearbox = choice(gearbox_list)
        ogrn_showroom = choice(showroom_list)[0]
        auto_list.append([vin, keys[key_ind], auto[model][key_model][0], price, year, transmission, gearbox, ogrn_showroom])

    print("List of automobiles - Successfully")
    return auto_list