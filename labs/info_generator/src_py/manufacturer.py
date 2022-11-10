from mimesis import Text, Person
from faker import Faker
from random import randint, choice


def parse_brand_string(string, counter):
    index = []
    for i in range(len(string)):
        if string[i] == "|":
            index.append(i)

    brand = string[0:index[0] - 1]
    country = string[index[0] + 2:index[1] - 1]
    year = string[index[1] + 2:index[2] - 1]
    founder = string[index[2] + 2:len(string) - 1]

    return [brand, country, year, founder]


def check_unique_brand(manufacturers_list, brand):
    for i in range(len(manufacturers_list)):
        if brand == manufacturers_list[i][0]:
            return 1
    return 0


def generate_manufacturers(number):
    file = open("../data/manufacturers.txt", "r", encoding="utf8")
    manufacturers_list = []
    counter = 0
    for string in file:
        manufacturers_list.append(parse_brand_string(string, counter))
        counter += 1
    number -= len(manufacturers_list)

    text = Text('nl')
    fake_ru = Faker('ru_RU')
    person_list = [Person('de'), Person('en'), Person('it'), Person('ru')]

    for _ in range(number):
        person = choice(person_list)

        brand = text.word().title()
        while check_unique_brand(manufacturers_list, brand) == 1:
            brand = text.word().title()
        country = fake_ru.country()
        year = randint(1850, 2010)
        founder = person.full_name()
        manufacturers_list.append([brand, country, year, founder])
        counter += 1
    print("List of manufacturers - Successfully")
    return manufacturers_list