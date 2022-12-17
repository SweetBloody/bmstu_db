from info_generator.src_py.manufacturer import generate_manufacturers
from info_generator.src_py.csv_proc import get_csv
import time
import csv


def input_mask_to_csv(filename):
    mask = [["brand", "country", "found_year", "founder"]]
    with open("../nifi/in_file/{}".format(filename), "w", newline="", encoding="utf8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(mask)


if __name__ == "__main__":
    number = 10
    count = 0
    while True:
        # filename = "manufacturers_lab8_{}.csv".format(count)
        filename = "manufacturers_lab8.csv"
        manufacturers_list = generate_manufacturers(number, 8)
        input_mask_to_csv(filename)
        get_csv(manufacturers_list, filename, 8)
        count += 1
        time.sleep(30)


