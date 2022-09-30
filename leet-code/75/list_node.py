from typing import List, Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next: Optional["ListNode"] = next

    @classmethod
    def array_to_listnode(
        cls, array: List[int], circle_index: Optional[int] = None
    ) -> Optional["ListNode"]:
        l1_head = dummly_l1 = cls(val=array[0])
        node_list = []
        for i in range(1, len(array)):
            new_l1 = cls(val=array[i])
            l1_head.next = new_l1
            node_list.append(l1_head)
            l1_head = new_l1
        if circle_index:
            l1_head.next = node_list[circle_index]
        return dummly_l1

    def __str__(self):
        return f"Node value: {self.val}"
