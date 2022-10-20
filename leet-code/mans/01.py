from timer import Timer


def find_missing_int_naive(lst):
    #  space comp O(n)
    missing_int_set = set(lst)
    #  space comp O(n)
    int_set = {i for i in range(1, len(lst) + 2)}
    #  time comp O(n)
    missing_int = int_set.difference(missing_int_set)
    if not missing_int:
        return None
    iterator = iter(missing_int)
    return next(iterator)


def find_missing_int(lst):
    missing_sum = sum(lst)
    non_missing_sum = 0
    for i in range(1, len(lst) + 2):
        non_missing_sum += i
    return non_missing_sum - missing_sum


def find_missing_formula(lst):
    n = len(lst) + 1
    sum_total = n * (n + 1) // 2
    return sum_total - sum(lst)


if __name__ == "__main__":
    missing_int = [1, 2, 6, 7, 9, 3, 4, 10, 8]
    # missed = find_missing_int_naive(missing_int)
    with Timer("Method shit"):
        missed = find_missing_int_naive(missing_int)
        assert missed == 5
    with Timer("Method sum"):
        missed = find_missing_int(missing_int)
        assert missed == 5
    with Timer("Method formula"):
        missed = find_missing_formula(missing_int)
        assert missed == 5
