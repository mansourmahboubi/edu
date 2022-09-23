import time
from typing import List


class Solution:
    def pivot_index(self, nums: List[int]) -> int:
        sum_nums = sum(nums)
        left_sum = 0
        for index in range(len(nums)):
            right_sum = sum_nums - left_sum - nums[index]
            if left_sum == right_sum:
                return index
            left_sum += nums[index]

        return -1

    def pivot_index_1(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        sumL = 0
        sumR = sum(nums)
        for i in range(len(nums)):
            sumR -= nums[i]
            if sumL == sumR:
                return i
            sumL += nums[i]
        return -1

    def pivot_index_2(self, nums):
        S = sum(nums)
        leftsum = 0
        for i, x in enumerate(nums):
            if leftsum == (S - leftsum - x):
                return i
            leftsum += x
        return -1


if __name__ == "__main__":
    s = Solution()
    sample = [1, 7, 3, 6, 5, 6]
    start = time.perf_counter_ns()
    res = s.pivot_index(sample)
    print(res)
    end = time.perf_counter_ns()
    print(f"method 1 {end-start} ns")

    start = time.perf_counter_ns()
    res = s.pivot_index_1(sample)
    print(res)
    end = time.perf_counter_ns()
    print(f"method 2 {end-start} ns")

    start = time.perf_counter_ns()
    res = s.pivot_index_2(sample)
    print(res)
    end = time.perf_counter_ns()
    print(f"method 3 {end-start} ns")
