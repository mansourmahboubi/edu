from typing import List


# Definition for a Node.
class NAryNode:
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
            if array[i] == None:  # noqa: E711
                index += 1
            else:
                node = cls(array[i], children=[])
                nodes.append(node)
                nodes[index].children.append(node)  # type:ignore
                # print(f"self: {node.val} parent: {nodes[index].val}")
        return root
