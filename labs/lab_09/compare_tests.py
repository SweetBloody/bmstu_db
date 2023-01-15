import time
import matplotlib
import matplotlib.pyplot as plt
from views import get_young_cust, delete_last_cust, add_cust, change_cust, get_young_cust_cache

matplotlib.use('tkagg')

N = 50
SLEEP_TIME = 2
STEP = 10

cached_time = []
not_cached_time = []

def select(connection, r):
    start = time.time()
    get_young_cust(connection, r)
    not_cached_time.append(time.time() - start)


def select_cached(connection, r):
    start = time.time()
    get_young_cust_cache(connection, r)
    cached_time.append(time.time() - start)

def insert(connection, r):
    start = time.time()
    add_cust(connection, r)
    cached_time.append(time.time() - start)

def delete(connection, r):
    start = time.time()
    delete_last_cust(connection, r)
    cached_time.append(time.time() - start)

def update(connection, r):
    start = time.time()
    change_cust(connection, r)
    cached_time.append(time.time() - start)

def benchmark_select(connection, r):
    global cached_time, not_cached_time
    cached_time, not_cached_time = [], []

    for i in range(N):
        select(connection, r)

    for i in range(N):
        select_cached(connection, r)

    plt.plot(range(len(cached_time)), cached_time, label="Select с кешированием")
    plt.plot(range(len(not_cached_time)), not_cached_time, label="Select без кеширования")
    plt.legend()
    plt.savefig('./select.png')


    plt.clf()

def benchmark_insert(connection, r):
    global cached_time, not_cached_time
    cached_time, not_cached_time = [], []

    for i in range(N):
        select(connection, r)
        select_cached(connection, r)

        time.sleep(SLEEP_TIME)

        if i % STEP == 0:
            insert(connection, r)

    plt.plot(range(len(cached_time)), cached_time, label="Insert + select с кешированием")
    plt.plot(range(len(not_cached_time)), not_cached_time, label="Insert + select без кеширования")
    plt.legend()
    plt.savefig('./insert-select.png')

    plt.clf()

def benchmark_update(connection, r):
    global cached_time, not_cached_time
    cached_time, not_cached_time = [], []

    for i in range(N):
        select(connection, r)
        select_cached(connection, r)

        time.sleep(SLEEP_TIME)

        if i % STEP == 0:
            update(connection, r)

    plt.plot(range(len(cached_time)), cached_time, label="update + select с кешированием")
    plt.plot(range(len(not_cached_time)), not_cached_time, label="update + select без кеширования")
    plt.legend()
    plt.savefig('./update-select.png')

    plt.clf()

def benchmark_delete(connection, r):
    global cached_time, not_cached_time
    cached_time, not_cached_time = [], []

    for i in range(N):
        select(connection, r)
        select_cached(connection, r)

        time.sleep(SLEEP_TIME)

        if i % STEP == 0:
            delete(connection, r)

    plt.plot(range(len(cached_time)), cached_time, label="delete + select с кешированием")
    plt.plot(range(len(not_cached_time)), not_cached_time, label="delete + select без кеширования")
    plt.legend()
    plt.savefig('./delete-select.png')

    plt.clf()

def benchmark(connection, r):
    benchmark_select(connection, r)
    benchmark_insert(connection, r)
    benchmark_delete(connection, r)
    for i in range(N // STEP):
        insert(connection, r)
    benchmark_update(connection, r)

