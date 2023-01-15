from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import json
from views import get_young_cust, delete_last_cust, add_cust, change_cust, get_young_cust_cache
from compare_tests import benchmark
import db_connection
import redis

cfg = json.load(open("./config.json"))
DB_INFO = cfg['db']

engine = create_engine(
    f'postgresql://{DB_INFO["user"]}:{DB_INFO["password"]}@{DB_INFO["host"]}:{DB_INFO["port"]}',
    pool_pre_ping=True)

r = redis.Redis()

Session = sessionmaker(bind=engine)

QUERIES = {
    1: get_young_cust,
    2: get_young_cust_cache,
    3: delete_last_cust,
    4: add_cust,
    5: change_cust,
}



def main():
    connection = db_connection.connect(DB_INFO)
    benchmark(connection, r)
    connection.close()


if __name__ == "__main__":
    main()

