def find_year(string):
    index_z = 0
    index_t = 0
    for i in range(len(string)):
        if string[i] == ",":
            index_z = i
        if string[i] == "-":
            index_t = i
    b_year = int(string[index_z + 2 : index_z + 6])
    if string[index_t + 2:len(string)] != "сегодня\n":
        e_year = int(string[index_t + 2:index_t + 6])
    else:
        e_year = 2022
    return b_year, e_year


def parse_auto_file():
    file = open("../data/automobiles.txt", "r", encoding="utf8")
    flag = 0
    model = ""
    brand = ""
    automobiles = {}
    models_array = []
    for string in file:
        if flag == 2:
            b_year, e_year = find_year(string)
            models_array.append([model, b_year, e_year])
            flag = 1
        elif flag == 1:
            if string == "---\n":
                automobiles[brand] = models_array
                models_array = []
                flag = 0
            else:
                model = string[:-1]
                flag = 2
        else:
            brand = string[:-1]
            flag = 1
    file.close()

    return automobiles
