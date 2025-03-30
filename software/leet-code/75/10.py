"""
Given a string s which consists of lowercase or uppercase letters, return the length of the longest palindrome that can be built with those letters.

Letters are case sensitive, for example, "Aa" is not considered a palindrome here.
"""

from collections import Counter

from timer import Timer


class Solution:
    def longest_palindrome_1(self, s: str) -> int:
        c = Counter(s)

        max_pal = 0
        alone_letter = False
        for letter, count in c.items():
            half = count / 2
            max_pal += int(half)
            if not half == int(half):
                alone_letter = True

        max_pal = int(max_pal) * 2
        if alone_letter:
            max_pal += 1
        return max_pal

    def longest_palindrome_2(self, s):
        odds = sum(v & 1 for v in Counter(s).values())
        return len(s) - odds + bool(odds)

    def longest_palindrome_3(self, s):
        ss = set()
        for letter in s:
            if letter not in ss:
                ss.add(letter)
            else:
                ss.remove(letter)
        if len(ss) != 0:
            return len(s) - len(ss) + 1
        else:
            return len(s)


if __name__ == "__main__":
    s = Solution()
    a = "abccccdd"

    with Timer("Method 1"):
        res = s.longest_palindrome_1(a)
        print(res)

    with Timer("Method 2"):
        res = s.longest_palindrome_2(a)
        print(res)

    with Timer("Method 3"):
        res = s.longest_palindrome_3(a)
        print(res)
