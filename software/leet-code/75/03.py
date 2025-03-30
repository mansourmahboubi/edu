import time


class Solution:
    def is_isomorphic(self, s: str, t: str) -> bool:
        hashmap = {}
        for index in range(len(s)):
            frist_letter = s[index]
            second_letter = t[index]
            if not second_letter in hashmap.values():
                hashmap[frist_letter] = second_letter
        isom = ""
        for letter in s:
            if letter in hashmap:
                isom += hashmap[letter]
        if isom == t:
            return True
        return False

    def is_isomorphic_1(self, s: str, t: str) -> bool:
        mapping_s_t = {}
        mapping_t_s = {}

        for c1, c2 in zip(s, t):

            # Case 1: No mapping exists in either of the dictionaries
            if (c1 not in mapping_s_t) and (c2 not in mapping_t_s):
                mapping_s_t[c1] = c2
                mapping_t_s[c2] = c1

            # Case 2: Ether mapping doesn't exist in one of the dictionaries or Mapping exists and
            # it doesn't match in either of the dictionaries or both
            elif mapping_s_t.get(c1) != c2 or mapping_t_s.get(c2) != c1:
                return False

        return True

    def transform_string(self, s: str) -> str:
        index_mapping = {}
        new_str = []

        for i, c in enumerate(s):
            if c not in index_mapping:
                index_mapping[c] = i
            new_str.append(str(index_mapping[c]))

        return " ".join(new_str)

    def is_isomorphic_2(self, s: str, t: str) -> bool:
        return self.transform_string(s) == self.transform_string(t)


if __name__ == "__main__":
    s = Solution()
    start = time.perf_counter_ns()
    res = s.is_isomorphic("egg", "add")
    print(res)
    end = time.perf_counter_ns()
    print(f"method 1 {end-start} ns")

    start = time.perf_counter_ns()
    res = s.is_isomorphic_1("egg", "add")
    print(res)
    end = time.perf_counter_ns()
    print(f"method 2 {end-start} ns")

    start = time.perf_counter_ns()
    res = s.is_isomorphic_2("egg", "add")
    print(res)
    end = time.perf_counter_ns()
    print(f"method 3 {end-start} ns")
