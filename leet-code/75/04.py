import time
from itertools import accumulate
from typing import List


class Solution:
    def is_subsequence(self, s: str, t: str) -> bool:
        index = None
        string = ""
        for l in s:
            after_letters = t[index + 1 if index else 0 : len(t)]
            if l in after_letters:
                cur_index = after_letters.index(l) + (len(t) - len(after_letters))
                if not index or cur_index > index:
                    string += l
                    index = cur_index
                else:
                    return False
        if string == s:
            return True
        return False

    def is_subsequence_2(self, s: str, t: str) -> bool:
        i, j = 0, 0
        while i < len(s) and j < len(t):
            if s[i] == t[j]:
                i += 1
            j += 1
        return i == len(s)


if __name__ == "__main__":
    s = Solution()
    a = "twdn"
    b = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxtxxxxxxxxxxxxxxxxxxxxwxxxxxxxxxxxxxxxxxxxxxxxxxn"
    start = time.perf_counter_ns()
    res = s.is_subsequence(a, b)
    print(res)
    end = time.perf_counter_ns()
    print(f"method 1 {end-start} ns")

    start = time.perf_counter_ns()
    res = s.is_subsequence_2(a, b)
    print(res)
    end = time.perf_counter_ns()
    print(f"method 2 {end-start} ns")
