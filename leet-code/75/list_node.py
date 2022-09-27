from typing import List, Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next: Optional["ListNode"] = next

    @classmethod
    def array_to_listnode(cls, array: List[int]) -> Optional["ListNode"]:
        l1_head = dummly_l1 = cls(val=array[0])
        for i in range(1, len(array)):
            new_l1 = cls(val=array[i])
            l1_head.next = new_l1
            l1_head = new_l1
        return dummly_l1

    def __str__(self):
        return f"{self.val}-{self.next}"
