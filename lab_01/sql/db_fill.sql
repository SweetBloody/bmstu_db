copy public.manufacturers(
    brand,
    country,
    found_year,
    founder)
from '/db_data/csv_files/manufacturers.csv' delimiter ',' CSV;

copy public.customers(
    id,
    surname,
    first_name,
    otch,
    age,
    sex)
from '/db_data/csv_files/customers.csv' delimiter ',' CSV;

copy public.showrooms(
    ogrn, --13
    full_name,
    address,
    owner_id,
    brand)
from '/db_data/csv_files/showrooms.csv' delimiter ',' CSV;

copy public.automobiles(
    vin,
    brand,
    model,
    price,
    prod_year,
    transmission,
    gearbox,
	showroom_ogrn)
from '/db_data/csv_files/autos.csv'  delimiter ',' CSV;

copy public.engines(
    vin,
    power,
    cylinders,
    capacity,
    consumption)
from '/db_data/csv_files/engines.csv' delimiter ',' CSV;

copy public.customers_showrooms(
    customer_id,
    showroom_ogrn)
from '/db_data/csv_files/customers_showroom.csv' delimiter ',' CSV;
