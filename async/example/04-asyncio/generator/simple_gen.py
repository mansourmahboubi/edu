from typing import Generator, List

from mansour_utils.timer import Timer


def fib(n: int) -> List[int]:
    numbers = []
    current, nxt = 0, 1
    while len(numbers) < n:
        current, nxt = nxt, current + nxt
        numbers.append(current)

    return numbers


def fib_gen() -> Generator[int, None, None]:
    current, nxt = 0, 1
    while True:
        current, nxt = nxt, current + nxt
        yield current


with Timer("Method 1"):
    result = fib(21)
    print(result)

with Timer("Method gen"):
    result = fib_gen()
    print(result)

    for n in result:
        print(n, end=", ")
        if n > 10000:
            break
    print("")

print()
print("Done")
