class Tree:
    """
    Дерево для метода ветвей и границ
    """

    def __init__(self):
        self.root = None

    def add_node(self, node, left, right):
        self.root = Node(node, left, right)


class Node:
    """
    Узел дерева
    """

    def __init__(self, node, left, right):
        self.node = None
        self.left = None
        self.right = None
