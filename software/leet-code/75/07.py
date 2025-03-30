"""
Given the head of a singly linked list, return the middle node of the linked list.

If there are two middle nodes, return the second middle node.
"""
from typing import Optional

from list_node import ListNode
from timer import Timer


class Solution:
    def middle_node(self, head: Optional[ListNode]) -> Optional[ListNode]:
        tmp = head
        counter = 0
        while tmp:
            counter += 1
            tmp = tmp.next

        middle_node = counter // 2

        tmp_2 = head
        for i in range(middle_node):
            tmp_2 = tmp_2.next  # type:ignore

        return tmp_2

    def middle_node_1(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Each time, slow go 1 steps while fast go 2 steps.
        When fast arrives at the end, slow will arrive right in the middle.
        """
        slow = fast = head
        while fast and fast.next:
            slow = slow.next  # type:ignore
            fast = fast.next.next
        return slow


if __name__ == "__main__":
    s = Solution()
    with Timer("Method 1"):
        a = [1, 2, 3, 4, 5]
        node_head_1 = ListNode.array_to_listnode(a)

        res = s.middle_node(node_head_1)
        print(res)

    with Timer("Method 2"):
        a = [1, 2, 3, 4, 5]
        node_head_1 = ListNode.array_to_listnode(a)

        res = s.middle_node_1(node_head_1)
        print(res)
