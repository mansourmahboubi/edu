import sys
from concurrent.futures import ThreadPoolExecutor
from threading import active_count, current_thread
from time import perf_counter, sleep

DAEMON_BOOL = False
start = perf_counter()


def show(name, sleep_seconds=3):
    print(f"{name} started")
    sleep(sleep_seconds)
    print(current_thread())
    print(f"{name} finished")


# thread module
# t1 = Thread(target=show, args=('t1',5),name='shoobool', daemon=DAEMON_BOOL)
# t2 = Thread(target=show, args=('t2',),name='bala', daemon=DAEMON_BOOL)

# t1.start()
# t2.start()

# pool executer

with ThreadPoolExecutor(max_workers=2) as executor:
    names = ["t1", "t2", "t3"]
    executor.map(show, names)

end = perf_counter()

print(f"Elapsed time: {end - start}")
print(f"Threads alive: {active_count()}")
sys.exit()
