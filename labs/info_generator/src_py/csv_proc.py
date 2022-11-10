import csv


def get_csv(list, filename):
    with open("../../csv_files/{}".format(filename), "w", newline="", encoding="utf8") as file:
        writer = csv.writer(file)
        writer.writerows(list)
    print("{} - Successfully".format(filename))

