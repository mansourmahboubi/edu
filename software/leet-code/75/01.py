import time
from itertools import accumulate
from typing import List


class Solution:
    def running_sum(self, nums: List[int]) -> List[int]:
        for index in range(1, len(nums)):
            nums[index] = nums[index] + nums[index - 1]
        return nums

    def running_sum_1(self, nums: List[int]) -> List[int]:
        """
        using python accumulate module
        """
        return list(accumulate(nums))

    def running_sum_2(self, nums):
        return [sum(nums[: i + 1]) for i in range(len(nums))]


if __name__ == "__main__":
    s = Solution()
    sample = [3, 1, 2, 10, 1]
    start = time.perf_counter_ns()
    res = s.running_sum(sample)
    print(res)
    end = time.perf_counter_ns()
    print(f"method 1 {end-start} ns")

    start = time.perf_counter_ns()
    res = s.running_sum_1(sample)
    print(res)
    end = time.perf_counter_ns()
    print(f"method 2 {end-start} ns")

    start = time.perf_counter_ns()
    res = s.running_sum_2(sample)
    print(res)
    end = time.perf_counter_ns()
    print(f"method 3 {end-start} ns")
