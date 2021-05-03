from data_structures.ds3 import LinkedBinaryTree
from math import log2, floor


class ExpressionTree(LinkedBinaryTree):

    def __init__(self, token, left=None, right=None):
        super().__init__()
        if not isinstance(token, str):
            raise TypeError("Token Must be a string")
        self.add_root(token)

        assert not ((right is None) ^ (left is None))
        assert not ((right is not None) ^ (left is not None))

        if left is not None:
            if token not in "+-*/":
                raise ValueError(f"{token} is not a valid token")
            self.attach(self.get_root(), left, right)

    def __str__(self):
        tokens = []
        self.parenthesize(self.get_root(), tokens)
        return 'ExpressionTree' + ''.join(tokens)

    def parenthesize(self, node, tokens):
        if self.is_leaf(node):
            tokens.append(str(node.element))
        else:
            tokens.append('(')
            self.parenthesize(self.get_left(node), tokens)
            tokens.append(str(node.element))
            self.parenthesize(self.get_right(node), tokens)
            tokens.append(')')

    def evaluate(self):
        def run(node):
            if self.is_leaf(node):
                return float(node.element)
            else:
                left_val = run(self.get_left(node))
                right_val = run(self.get_right(node))
                op = node.element
                return eval(f"{left_val} {op} {right_val}")

        return run(self.get_root())

    def draw(self, indent=1):
        previous_level = -1
        for i, node in enumerate(self.breadthfirst(), 1):
            if i == 1:
                print(f"{str(node.element).rjust(self.size)}")
                previous_level = 0
            else:
                level = floor(log2(i))
                num_nodes = 2 ** level
                subdiv = (2 * self.size) // (num_nodes + 1)
                _, position = divmod(i, num_nodes)
                if previous_level != level:
                    print()
                    print()
                    previous_level = level
                print(f"{str(node.element).rjust((position + 1) * subdiv)}", end="")
