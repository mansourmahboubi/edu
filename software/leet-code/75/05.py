from typing import Optional

from list_node import ListNode
from timer import Timer


class Solution:
    def merge_two_lists(
        self,
        l1: Optional["ListNode"],
        l2: Optional["ListNode"],
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
        dummly_l1 = ListNode.array_to_listnode(a)
        dummly_l2 = ListNode.array_to_listnode(b)
        res = s.merge_two_lists(dummly_l1, dummly_l2)
        print(res)
