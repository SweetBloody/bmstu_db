from random import randint, random


def generate_engine(vin):
    min_power = 80
    max_power = 250
    min_capacity = 1
    max_capacity = 5
    consumption = 7
    power = randint(min_power, max_power)
    cylinders = randint(4, 8)
    capacity = random() * (max_capacity - min_capacity) + min_capacity
    if 1 <= capacity < 2:
        consumption = 6.1
    elif 2 <= capacity < 3:
        consumption = 6.3
    elif 3 <= capacity < 4:
        consumption = 8.1
    elif 4 <= capacity <= 5:
        consumption = 11.8
    return [vin, power, cylinders, int(capacity * 10) / 10, consumption]


def generate_engines(auto_list):
    engines_list = []
    for auto in auto_list:
        engines_list.append(generate_engine(auto[0]))
    print("List of engines - Successfully")
    return engines_list

