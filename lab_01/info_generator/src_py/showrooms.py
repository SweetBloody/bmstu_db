from faker import Faker
from random import choice, randint


def generate_unique_ogrn(number):
    ogrn_list = []
    fake_ru = Faker('ru_RU')
    for _ in range(number):
        flag = 1
        while flag == 1:
            flag = 0
            ogrn = fake_ru.businesses_ogrn()
            for i in range(len(ogrn_list)):
                if ogrn == ogrn_list[i]:
                    flag = 1
                    break
            flag = 0
        ogrn_list.append(fake_ru.businesses_ogrn())
    return ogrn_list


def get_owner_id(owners_id_list, number):
    flag = 1
    id = 0
    while flag == 1:
        flag = 0
        id = randint(1, number)
        for i in range(len(owners_id_list)):
            if id == owners_id_list[i]:
                flag = 1
                break
    return id


def generate_showrooms(number, number_cust, manufacturers_list):
    showrooms_list = []
    fake_ru = Faker('ru_RU')
    fake = Faker()
    ogrn_list = generate_unique_ogrn(number)
    owners_id_list = []
    for i in range(number):
        ogrn = ogrn_list[i]
        address = fake_ru.address()
        name = fake.company()
        owner_id = get_owner_id(owners_id_list, number_cust)
        owners_id_list.append(owner_id)
        if randint(0, 1) == 1:
            brand = choice(manufacturers_list)[0]
        else:
            brand = ""
        showrooms_list.append([ogrn, name, address, owner_id, brand])
    print("List of showrooms - Successfully")
    return showrooms_list

