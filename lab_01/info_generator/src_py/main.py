from file_parser import parse_auto_file
from showrooms import generate_showrooms
from manufacturer import generate_manufacturers
from customers import generate_customers, generate_customers_showroom
from automobiles import generate_autos
from engines import generate_engines
from csv_proc import get_csv

if __name__ == '__main__':
    auto = parse_auto_file()

    number = 1000
    number_cust = 3000


    manufacturers_list = generate_manufacturers(number)
    customers_list, customer_ind = generate_customers(number_cust)
    showroom_list = generate_showrooms(number, number_cust, manufacturers_list)
    auto_list = generate_autos(auto, number, showroom_list)
    engines_list = generate_engines(auto_list)
    cust_show_list = generate_customers_showroom(customer_ind, showroom_list)

    get_csv(auto_list, "autos.csv")
    get_csv(engines_list, "engines.csv")
    get_csv(customers_list, "customers.csv")
    get_csv(manufacturers_list, "manufacturers.csv")
    get_csv(showroom_list, "showrooms.csv")
    get_csv(cust_show_list, "customers_showroom.csv")

