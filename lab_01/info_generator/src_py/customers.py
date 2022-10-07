from random import randint
import numpy as np


def prepare(showroom_list):
    arr = []
    for elem in showroom_list:
        arr.append(elem[0])
    return arr


def generate_customers_showroom(customers_ind, showroom_list):
    cust_show_list = []
    ogrns = prepare(showroom_list)
    for i in range(len(customers_ind)):
        num = randint(1, 5)
        arr = np.random.choice(ogrns, num, replace=False)
        for elem in arr:
            cust_show_list.append([customers_ind[i], elem])
    print("List of customers_showrooms - Successfully")
    return cust_show_list


def generate_customers(number):
    MALE_NAMES = ['Александр', 'Алексей', 'Анатолий', 'Андрей', 'Антон', 'Аркадий', 'Артем', 'Борислав', 'Вадим', 'Валентин', 'Валерий', 'Василий', 'Виктор', 'Виталий', 'Владимир', 'Вячеслав', 'Геннадий', 'Георгий', 'Григорий', 'Даниил', 'Денис', 'Дмитpий', 'Евгений', 'Егор', 'Иван', 'Игорь', 'Илья', 'Кирилл', 'Лев', 'Максим', 'Михаил', 'Никита', 'Николай', 'Олег', 'Семен', 'Сергей', 'Станислав', 'Степан', 'Федор', 'Юрий']
    FEMALE_NAMES = ['Александра', 'Алина', 'Алла', 'Анастасия', 'Анжела', 'Анна', 'Антонина', 'Валентина', 'Валерия', 'Вероника', 'Виктория', 'Галина', 'Дарья', 'Евгения', 'Екатерина', 'Елена', 'Елизавета', 'Карина', 'Кира', 'Клавдия', 'Кристина', 'Ксения', 'Лидия', 'Любовь', 'Людмила', 'Маргарита', 'Марина', 'Мария', 'Надежда', 'Наталья', 'Нина', 'Оксана', 'Олеся', 'Ольга', 'Полина', 'Светлана', 'Таисия', 'Тамара', 'Татьяна', 'Эвелина', 'Эльвира', 'Юлиана', 'Юлия', 'Яна']
    SURNAMES = ['Смирнов', 'Иванов', 'Кузнецов', 'Соколов', 'Попов', 'Лебедев', 'Козлов', 'Новиков', 'Морозов', 'Петров', 'Волков', 'Соловьёв', 'Васильев', 'Зайцев', 'Павлов', 'Семёнов', 'Голубев', 'Виноградов', 'Богданов', 'Воробьёв', 'Фёдоров', 'Михайлов', 'Беляев', 'Тарасов', 'Белов', 'Комаров', 'Орлов', 'Киселёв', 'Макаров', 'Андреев', 'Ковалёв', 'Ильин', 'Гусев', 'Титов', 'Кузьмин', 'Кудрявцев', 'Баранов', 'Куликов', 'Алексеев', 'Степанов', 'Яковлев', 'Сорокин', 'Сергеев', 'Романов', 'Захаров', 'Борисов', 'Королёв', 'Герасимов', 'Пономарёв', 'Григорьев', 'Лазарев', 'Медведев', 'Ершов', 'Никитин', 'Соболев', 'Рябов', 'Поляков', 'Цветков', 'Данилов', 'Жуков', 'Фролов', 'Журавлёв', 'Николаев', 'Крылов', 'Максимов', 'Сидоров', 'Осипов', 'Белоусов']
    MALE_OTCH = ['Александрович', 'Алексеевич', 'Анатольевич', 'Андреевич', 'Антонович', 'Аркадьевич', 'Арсеньевич', 'Артемович', 'Афанасьевич', 'Богданович', 'Борисович', 'Вадимович', 'Валентинович', 'Валериевич', 'Васильевич', 'Викторович', 'Витальевич', 'Владимирович', 'Всеволодович', 'Вячеславович', 'Гаврилович', 'Геннадиевич', 'Георгиевич', 'Глебович', 'Григорьевич', 'Давыдович', 'Данилович', 'Денисович', 'Дмитриевич', 'Евгеньевич', 'Егорович', 'Емельянович', 'Ефимович', 'Иванович', 'Игоревич', 'Ильич', 'Иосифович', 'Кириллович', 'Константинович', 'Корнеевич', 'Леонидович', 'Львович', 'Макарович', 'Максимович', 'Маркович', 'Матвеевич', 'Митрофанович', 'Михайлович', 'Назарович', 'Наумович', 'Николаевич', 'Олегович', 'Павлович', 'Петрович', 'Платонович', 'Робертович', 'Родионович', 'Романович', 'Савельевич', 'Семенович', 'Сергеевич', 'Станиславович', 'Степанович', 'Тарасович', 'Тимофеевич', 'Тихонович', 'Федорович', 'Феликсович', 'Филиппович', 'Эдуардович', 'Юрьевич', 'Яковлевич', 'Ярославович']
    FEMALE_OTCH = ['Александровна', 'Алексеевна', 'Анатольевна', 'Андреевна', 'Антоновна', 'Аркадьевна', 'Арсеньевна', 'Афанасьевна', 'Богдановна', 'Борисовна', 'Валентиновна', 'Валериевна', 'Васильевна', 'Викторовна', 'Владимировна', 'Владиславовна', 'Вячеславовна', 'Геннадиевна', 'Георгиевна', 'Григорьевна', 'Даниловна', 'Дмитриевна', 'Евгеньевна', 'Егоровна', 'Ефимовна', 'Ивановна', 'Игоревна', 'Ильинична', 'Иосифовна', 'Кирилловна', 'Константиновна', 'Леонидовна', 'Львовна', 'Максимовна', 'Матвеевна', 'Михайловна', 'Николаевна', 'Олеговна', 'Павловна', 'Петровна', 'Платоновна', 'Робертовна', 'Романовна', 'Семеновна', 'Сергеевна', 'Станиславовна', 'Степановна', 'Тарасовна', 'Тимофеевна', 'Федоровна', 'Фелuксовна', 'Филипповна', 'Эдуардовна', 'Юрьевна', 'Яковлевна', 'Ярославовна']
    customers_list = []
    customer_ind = []
    for i in range(number):
        sex = randint(0, 1)
        if sex == 0:
            name_ind = randint(0, len(MALE_NAMES) - 1)
            surname_ind = randint(0, len(SURNAMES) - 1)
            otch_ind = randint(0, len(MALE_OTCH) - 1)
            surname = SURNAMES[surname_ind]
            name = MALE_NAMES[name_ind]
            otch = MALE_OTCH[otch_ind]
            sex = 'мужской'
            age = randint(20, 60)
        else:
            name_ind = randint(0, len(FEMALE_NAMES) - 1)
            surname_ind = randint(0, len(SURNAMES) - 1)
            otch_ind = randint(0, len(FEMALE_OTCH) - 1)
            surname = SURNAMES[surname_ind] + 'а'
            name = FEMALE_NAMES[name_ind]
            otch = FEMALE_OTCH[otch_ind]
            sex = 'женский'
            age = randint(20, 60)
        customers_list.append([surname, name, otch, age, sex])
        customer_ind.append(i + 1)
    print("List of customers - Successfully")
    return customers_list, customer_ind
