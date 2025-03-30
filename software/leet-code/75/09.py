"""
You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.
"""
from typing import List

from timer import Timer


class Solution:
    def max_profit(self, prices: List[int]) -> int:
        max_profit = 0
        for i in range(len(prices)):
            for j in range(i, len(prices)):
                if prices[j] - prices[i] > max_profit:
                    max_profit = prices[j] - prices[i]
        return max_profit

    def max_profit_1(self, prices: List[int]) -> int:
        left = 0  # Buy
        right = 1  # Sell
        max_profit = 0
        while right < len(prices):
            currentProfit = prices[right] - prices[left]  # our current Profit
            if prices[left] < prices[right]:
                max_profit = max(currentProfit, max_profit)
            else:
                left = right
            right += 1
        return max_profit


if __name__ == "__main__":
    s = Solution()
    a = [7, 1, 5, 3, 6, 4]

    with Timer("Method 1"):
        res = s.max_profit(a)
        print(res)

    with Timer("Method 2"):
        res = s.max_profit_1(a)
        print(res)
