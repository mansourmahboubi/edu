import time
from typing import Optional

from timer import Timer


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next: Optional["ListNode"] = next

    def __str__(self):
        return f"{self.val}-{self.next}"


class Solution:
    def merge_two_lists(
        self, l1: Optional["ListNode"], l2: Optional["ListNode"]
    ) -> Optional["ListNode"]:
        tmp = head = ListNode()
        while l1 and l2:
            if l1.val < l2.val:
                tmp.next = l1
                l1 = l1.next
            else:
                tmp.next = l2
                l2 = l2.next
            tmp = tmp.next

        if l1 or l2:
            tmp.next = l1 if l1 else l2

        return head.next


if __name__ == "__main__":
    s = Solution()
    with Timer():
        a = [1, 2, 4]
        b = [1, 3, 4]
        l1_head = dummly_l1 = ListNode(val=1)
        l2_head = dummly_l2 = ListNode(val=1)
        for i in range(1, len(a)):
            new_l1 = ListNode(val=a[i])
            l1_head.next = new_l1
            l1_head = new_l1

            new_l2 = ListNode(val=b[i])
            l2_head.next = new_l2
            l2_head = new_l2
        res = s.merge_two_lists(dummly_l1, dummly_l2)
        print(res)
