"""
Given the head of a singly linked list, reverse the list, and return the reversed list.
"""
from typing import Optional

from list_node import ListNode
from timer import Timer


class Solution:
    def reverse_list(self, head: Optional["ListNode"]) -> Optional["ListNode"]:
        if not head:
            return head
        l1 = []
        tmp = head
        while tmp:
            l1.append(tmp.val)
            tmp = tmp.next
        l2 = l1[::-1]
        res = tmp = ListNode(val=l2[0])
        for i in range(1, len(l2)):
            new = ListNode(val=l2[i])
            tmp.next = new
            tmp = new
        return res

    def reverse_list_2(self, head: Optional["ListNode"]) -> Optional["ListNode"]:

        prev = None
        curr = head

        while curr:
            next = curr.next
            curr.next = prev
            prev = curr
            curr = next

        return prev

    def reverse_list_3(self, head, prev=None):
        """
        recurstion
        """
        if not head:
            return prev
        next = head.next
        head.next = prev
        return self.reverse_list_3(next, head)


if __name__ == "__main__":
    s = Solution()
    with Timer("Method 1"):
        a = [1, 2, 3, 4, 5]
        node_head_1 = ListNode.array_to_listnode(a)

        res = s.reverse_list(node_head_1)
        print(res)

    with Timer("Method 2"):
        a = [1, 2, 3, 4, 5]
        node_head_1 = ListNode.array_to_listnode(a)

        res = s.reverse_list_2(node_head_1)
        print(res)

    with Timer("Method 3"):
        a = [1, 2, 3, 4, 5]
        node_head_1 = ListNode.array_to_listnode(a)

        res = s.reverse_list_3(node_head_1)
        print(res)
