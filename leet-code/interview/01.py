import time
from itertools import accumulate
from typing import List


class Solution:
    def brute_force(self, nums: List[int], target: int) -> List[int]:
        """
        The brute force approach is simple. Loop through each element xxx and find if there is another value that equals to target−xtarget - xtarget−x.
        O(2)
        """
        for index in range(0, len(nums)):
            for s_index in range(index + 1, len(nums)):
                sum = nums[index] + nums[s_index]
                if sum == target:
                    return [index, s_index]
        return []

    def hash_map(self, nums: List[int], target: int) -> List[int]:
        """
        Time complexity: O(n). We traverse the list containing nnn elements exactly twice. Since the hash table reduces the lookup time to O(1)O(1)O(1), the overall time complexity is O(n).=
        Space complexity: O(n). The extra space required depends on the number of items stored in the hash table, which stores exactly nnn elements.
        """
        hashmap = {}
        for i in range(len(nums)):
            hashmap[nums[i]] = i
        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in hashmap and hashmap[complement] != i:
                return [i, hashmap[complement]]
        return []

    def one_way_hash_map(self, nums: List[int], target: int) -> List[int]:
        hashmap = {}
        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in hashmap:
                return [i, hashmap[complement]]
            hashmap[nums[i]] = i
        return []


if __name__ == "__main__":
    s = Solution()
    sample = [2, 1, 11, 15, 7]
    start = time.perf_counter_ns()
    res = s.brute_force(sample, 9)
    print(res)
    end = time.perf_counter_ns()
    print(f"method 1 {end-start} ns")

    start = time.perf_counter_ns()
    res = s.hash_map(sample, 9)
    print(res)
    end = time.perf_counter_ns()
    print(f"method 2 {end-start} ns")

    start = time.perf_counter_ns()
    res = s.one_way_hash_map(sample, 9)
    print(res)
    end = time.perf_counter_ns()
    print(f"method 3 {end-start} ns")
