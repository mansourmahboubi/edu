"""
Given the head of a linked list, return the node where the cycle begins. If there is no cycle, return null.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to (0-indexed). It is -1 if there is no cycle. Note that pos is not passed as a parameter.

Do not modify the linked list.
"""

from typing import Optional

from list_node import ListNode
from timer import Timer


class Solution:
    def detect_cycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        tmp = head
        hashmap = {}
        index = 0
        while tmp:
            hashmap[tmp] = index
            if tmp.next in hashmap:
                return tmp.next
            tmp = tmp.next
            index += 1
        return None

    def detect_cycle_1(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow, fast = (
                slow.next,
                fast.next.next,
            )  # type:ignore
            if slow == fast:
                break
        else:
            return None  # if not (fast and fast.next): return None

        while head != slow:
            head, slow = (
                head.next,
                slow.next,
            )  # type:ignore
        return head

    def detect_cycle_2(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next  # type:ignore
            fast = fast.next.next
            if slow == fast:
                slow = head
                while slow != fast:
                    slow = slow.next  # type:ignore
                    fast = fast.next  # type:ignore
                return slow


if __name__ == "__main__":
    s = Solution()
    a = [3, 2, 0, -4]
    circle_index = 1
    node_head_1 = ListNode.array_to_listnode(a, circle_index)

    with Timer("Method 1"):
        res = s.detect_cycle(node_head_1)
        print(res)

    with Timer("Method 2"):
        res = s.detect_cycle_1(node_head_1)
        print(res)

    with Timer("Method 3"):
        res = s.detect_cycle_2(node_head_1)
        print(res)
