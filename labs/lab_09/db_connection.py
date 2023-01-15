import psycopg2
from psycopg2 import OperationalError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        connection.rollback()
        return None

    return cursor


def connect(config):
    connection = psycopg2.connect(
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port']
    )

    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return connection

