drop table if exists manufacturers cascade;
create table public.manufacturers(
    brand varchar(30) not null primary key,
    country varchar(40) not null,
    found_year int check (found_year between 1000 and 2022),
    founder varchar(50)
);

drop table if exists customers cascade;
create table public.customers(
    id int generated always as identity primary key,
    surname varchar(15) not null,
    first_name varchar(15) not null,
    otch varchar(15),
    age int check (age > 0),
    sex text
);

drop table if exists showrooms cascade;
create table public.showrooms(
    ogrn varchar(13) not null primary key,
    full_name varchar(50) not null,
    address varchar(100) not null,
    owner_id int not null,
    brand varchar(30),

    foreign key (owner_id) references public.customers(id)
);

drop table if exists automobiles cascade;
create table public.automobiles(
    vin varchar(17) not null primary key,
    brand varchar(30) not null,
    model varchar(40) not null,
    price int check (price > 0),
    prod_year int check (prod_year between 1000 and 2022),
    transmission text,
    gearbox text,
	showroom_ogrn varchar(13) not null,
	anc_auto varchar(17),

    foreign key (brand) references public.manufacturers(brand),
	foreign key (showroom_ogrn) references public.showrooms(ogrn)
);

drop table if exists engines cascade;
create table public.engines(
    vin varchar(17) not null primary key,
    power int check (power > 0),
    cylinders int check (power > 0),
    capacity numeric(3, 1) check (capacity > 0),
    consumption numeric(3, 1) check (consumption > 0),

    foreign key (vin) references public.automobiles(vin)
);

drop table if exists customers_showrooms cascade;
create table public.customers_showrooms(
    customer_id int,
    showroom_ogrn varchar(13) not null,
	
	foreign key (customer_id) references public.customers(id),
	foreign key (showroom_ogrn) references public.showrooms(ogrn),
    primary key (customer_id, showroom_ogrn)
);
