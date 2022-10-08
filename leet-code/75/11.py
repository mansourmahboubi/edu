"""
Given the root of an n-ary tree, return the preorder traversal of its nodes' values.

Nary-Tree input serialization is represented in their level order traversal. Each group of children is separated by the null value (See examples)
https://www.tutorialspoint.com/python_data_structure/python_tree_traversal_algorithms.htm
https://www.studytonight.com/advanced-data-structures/nary-tree
"""

from typing import List

from timer import Timer


# Definition for a Node.
class Node:
    # intresting bug if children start with[]
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children

    # def __repr__(self):
    #     return f"value {self.val} childs {self.children} |"

    @classmethod
    def create_node_list_from_array(cls, array: List[int]):
        root = cls(array[0], children=[])
        nodes = [root]
        index = 0
        for i in range(2, len(array)):
            if array[i] == None:
                index += 1
            else:
                node = cls(array[i], children=[])
                nodes.append(node)
                nodes[index].children.append(node)  # type:ignore
                # print(f"self: {node.val} parent: {nodes[index].val}")
        return root


class Solution:
    def dfs(self, root, output):

        # If root is none return
        if root is None:
            return

        # for preorder we first add the root val
        output.append(root.val)

        # Then add all the children to the output
        for child in root.children:
            self.dfs(child, output)

    def preorder(self, root):
        """
        :type root: Node
        :rtype: List[int]
        """

        output = []

        # perform dfs on the root and get the output stack
        self.dfs(root, output)

        # return the output of all the nodes.
        return output

    def preorder_1(self, root):
        """
        :type root: Node
        :rtype: List[int]
        """
        if root is None:
            return []

        stack = [root]
        output = []
        # Till there is element in stack the loop runs.
        while stack:

            # pop the last element from the stack and store it into temp.
            temp = stack.pop()
            # append. the value of temp to output
            output.append(temp.val)

            # add the children of the temp into the stack in reverse order.
            # children of 1 = [3,2,4], if not reveresed then 4 will be popped out first from the stack.
            # if reversed then stack = [4,2,3]. Here 3 will pop out first.
            # This continues till the stack is empty.
            stack.extend(temp.children[::-1])

        # return the output
        return output


if __name__ == "__main__":
    s = Solution()
    a = [1, None, 3, 2, 4, None, 5, 6]

    n_ary = Node.create_node_list_from_array(a)

    with Timer("Method 1"):
        res = s.preorder(n_ary)
        print(res)

    with Timer("Method 2"):
        res = s.preorder_1(n_ary)
        print(res)

# b = [
#     1,
#     None,
#     2,
#     3,
#     4,
#     5,
#     None,
#     None,
#     6,
#     7,
#     None,
#     8,
#     None,
#     9,
#     10,
#     None,
#     None,
#     11,
#     None,
#     12,
#     None,
#     13,
#     None,
#     None,
#     14,
# ]
