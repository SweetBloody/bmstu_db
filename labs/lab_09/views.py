import datetime

import db_connection, random

CACHE_KEY = "cache"

QUERY_GET_ID_TEST_CUST = "SELECT id from customers where first_name = 'test name';"

QUERY_YOUNGEST_CUST = "select first_name from customers order by age desc limit 10;"

QUERY_DELETE_LAST_CUST = "delete from customers where id = (select id from automobiles where first_name = 'test name' order by age desc limit 1) returning id;"
QUERY_ADD_CUST = "insert into customers(surname, first_name, otch, age, sex) values ('{}', '{}', '{}', {}, '{}') returning id;"
QUERY_CHANGE_CUST = "update customers set first_name = 'change name' where id = {};"

def get_young_cust(connection, r):
    data = "Youngest cust: "
    cursor = db_connection.execute_query(connection, QUERY_YOUNGEST_CUST)
    if cursor is not None:
        res = cursor.fetchall()
        for auto in res:
            data += auto[0] + ", "
        data = data.rstrip(", ")
    return data

def get_young_cust_cache(connection, r):
    data = "Youngest cust: "
    redis_cache = r.get(CACHE_KEY)
    if redis_cache is not None:
        print("DATA FROM CACHE")
        return redis_cache.decode("utf-8")
    else:
        cursor = db_connection.execute_query(connection, QUERY_YOUNGEST_CUST)
        if cursor is not None:
            res = cursor.fetchall()
            for cust in res:
                data += cust[0] + ", "
            data = data.rstrip(", ")
        r.set(CACHE_KEY, data)
        return "NO DATA IN CACHE"


def delete_last_cust(connection, r):
    data = "Success deleted cust with id = {}"
    res = db_connection.execute_query(connection, QUERY_DELETE_LAST_CUST)
    res = res.fetchall()
    if len(res) == 0:
        return "NO TEST CUST"
    r.expire(CACHE_KEY, datetime.timedelta(seconds=0))
    return data.format(res[0][0])


def add_cust(connection, r):
    data = "Success add cust - id = {}"
    query = QUERY_ADD_CUST.format("test surname", "test cust", "test otch", random.randint(10, 85), random.choice(["женский", "мужской"]))
    res = db_connection.execute_query(connection, query)
    r.expire(CACHE_KEY, datetime.timedelta(seconds=0))

    return data.format(res.fetchall()[0][0])


def change_cust(connection, r):
    data = "Success change cust with id = {}"
    cust_id = []
    custs = db_connection.execute_query(connection, QUERY_GET_ID_TEST_CUST).fetchall()
    for row in custs:
        cust_id.append(row[0])
        
    id = random.randint(0, len(cust_id) - 1)

    db_connection.execute_query(connection, QUERY_CHANGE_CUST.format(cust_id[id]))

    r.expire(CACHE_KEY, datetime.timedelta(seconds=0))

    return data.format(cust_id[id])

