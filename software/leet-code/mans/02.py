"""
binary tree -  a tree which each node has at most 2 children
BST -
a) All the values in the left sub-tree has a value less than that of the root node.
b) All the values in the right node has a value greater than the value of the root node.
"""

from bst_node import BSTNode
from timer import Timer


def min_height_bst(lst, bst, start_idx, end_idx):
    if end_idx < start_idx:
        return

    min_point = (start_idx + end_idx) // 2
    value = lst[min_point]
    if bst is None:
        bst = BSTNode(value)
    else:
        bst.insert(value)

    min_height_bst(lst, bst, start_idx, min_point - 1)
    min_height_bst(lst, bst, min_point + 1, end_idx)
    return bst


def min_height_bst_2(lst, start, end):
    if end < start:
        return None

    mid = (start + end) // 2
    node = BSTNode(lst[mid])
    node.left = min_height_bst_2(lst, start, mid - 1)
    node.right = min_height_bst_2(lst, mid + 1, end)
    return node


if __name__ == "__main__":
    array = [1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 15, 19, 25, 32]
    with Timer("Method 1 bad"):
        bst = min_height_bst(array, None, 0, len(array) - 1)
    # bst.display()
    with Timer("Method 2 good"):
        bst = min_height_bst_2(array, 0, len(array) - 1)
    bst.display()
