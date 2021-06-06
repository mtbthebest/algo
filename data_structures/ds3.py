import abc


class TreeEmptyException(Exception):
    pass


class EmptyException(Exception):
    pass


class LinkedStack:
    class _Node:

        def __init__(self, element, next_node):
            self.element = element
            self.next = next_node

    def __init__(self):
        self.head = None
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def push(self, e):
        self.head = self._Node(e, self.head)
        self.size += 1

    def top(self):
        if self.is_empty():
            raise EmptyException("Empty Stack")
        return self.head.element

    def pop(self):
        if self.is_empty():
            raise EmptyException("Empty Stack")
        elem = self.head.element
        self.head = self.head.next
        self.size -= 1
        return elem


class LinkedQueue:
    class _Node:

        def __init__(self, element, next_node):
            self.element = element
            self.next = next_node

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def first(self):
        if self.is_empty():
            raise EmptyException("Empty Stack")
        return self.head.element

    def enqueue(self, e):
        node = self._Node(e, None)
        if self.is_empty():
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise EmptyException("Empty Stack")
        res = self.head.element
        self.head = self.head.next
        self.size -= 1
        if self.is_empty():
            self.tail = None

        return res


class DoublyLinkedBase:
    class _Node:
        def __init__(self, element, prev_node, next_node):
            self.element = element
            self.next = next_node
            self.prev_node = prev_node

    def __init__(self):
        self.header = self._Node(None, None, None)
        self.trailer = self._Node(None, None, None)
        self.header.next = self.trailer
        self.trailer.prev = self.header
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def insert_between(self, e, predecessor, successor):
        node = self._Node(e, predecessor, successor)
        predecessor.next = node
        successor.prev = node
        self.size += 1

        return node

    def delete(self, node):
        if self.size == 0:
            raise ValueError
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
        el = node.element
        node.prev = node.next = node.element = None
        return el


class Tree(abc.ABC):
    class Node:
        _id = 0

        def __new__(cls, *args, **kwargs):
            obj = super().__new__(cls)
            cls._id += 1
            obj._id = cls._id
            return obj

        def __init__(self, element, container=None):
            self.element = element
            self.container = container

        def __eq__(self, other):
            return type(self) == type(other) and self.element == other.element and \
                   self._id == other._id

        def __repr__(self):
            return f"Node(element={self.element})"

    def __len__(self):
        raise NotImplementedError

    def children(self, node):
        raise NotImplementedError

    def get_root(self):
        raise NotImplementedError

    def is_empty(self):
        return len(self) == 0

    def is_root(self, node):
        return node is self.get_root()

    def is_leaf(self, node):
        return self.num_children(node) == 0

    def num_children(self, node):
        raise NotImplementedError

    def get_parent(self, node):
        raise NotImplementedError

    def get_children(self, node):
        raise NotImplementedError

    def depth(self, node):
        if self.is_empty():
            raise ValueError
        if self.is_root(node):
            return 0
        return 1 + self.depth(self.get_parent(node))

    def height(self, node=None):
        node = self.get_root() if node is None else node
        if self.is_leaf(node):
            return 0
        return 1 + max(self.height(c) for c in self.children(node))

    def __iter__(self):
        for n in self.traversal():
            yield n.element

    def __repr__(self):
        for el in self:
            print(el)
        return ''

    def traversal(self):
        return self.preorder()

    def preorder(self):
        """Print parent before children and descent """
        if not self.is_empty():
            for node in self.subtree_preorder(self.get_root()):
                yield node

    def subtree_preorder(self, node):
        yield node
        for c in self.children(node):
            yield from self.subtree_preorder(c)

    def postorder(self):
        """Print children before parent """
        if not self.is_empty():
            for node in self.subtree_postorder(self.get_root()):
                yield node

    def subtree_postorder(self, node):
        for c in self.children(node):
            yield from self.subtree_postorder(c)
        yield node

    def breadthfirst(self):
        if not self.is_empty():
            lq = LinkedQueue()
            lq.enqueue(self.get_root())
            while not lq.is_empty():
                node = lq.dequeue()
                yield node
                for c in self.children(node):
                    lq.enqueue(c)


class BinaryTree(Tree):
    class Node(Tree.Node):
        __slots__ = ("parent", "left", "right")

        def __init__(self, element, parent=None, left=None, right=None):
            self.parent = parent
            self.left = left
            self.right = right
            super(BinaryTree.Node, self).__init__(element, self)

        @property
        def p(self):
            return self.parent

        def __repr__(self):
            return f"Node(element={self.element}," \
                   f"parent={self.parent.element if self.parent is not None else None}, " \
                   f"left={self.left.element if self.left is not None else None}," \
                   f"right={self.right.element if self.right is not None else None})"

    def get_left(self, node):
        raise NotImplementedError

    def get_right(self, node):
        raise NotImplementedError

    def get_parent(self, node):
        raise NotImplementedError

    def get_sibling(self, node):
        if (parent := node.p) is None:
            return None

        if (q := parent.get_left()) == node:
            return parent.get_right()
        else:
            return q

    def inorder(self):
        """Print left subtree, node, right subtree"""
        if not self.is_empty():
            for node in self.subtree_inorder(self.get_root()):
                yield node

    def subtree_inorder(self, node):
        if (left := self.get_left(node)) is not None:
            yield from self.subtree_inorder(left)
        yield node
        if (right := self.get_right(node)) is not None:
            yield from self.subtree_inorder(right)

    def traversal(self):
        return self.inorder()


class LinkedBinaryTree(BinaryTree):
    def __init__(self):
        self.root = None
        self.size = 0

    def get_root(self):
        return self.root

    def __len__(self):
        return self.size

    def add_root(self, el):
        node = self.Node(el)
        self.root = node
        self.size += 1
        return node

    def add_left(self, node, el):
        if node.left is not None:
            raise ValueError
        node.left = self.Node(el, node)
        self.size += 1
        return node.left

    def add_right(self, node, el):
        if node.right is not None:
            raise ValueError
        node.right = self.Node(el, node)
        self.size += 1
        return node.right

    def get_left(self, node):
        return node.left

    def get_right(self, node):
        return node.right

    def children(self, node):
        if node.left is not None:
            yield node.left
        if node.right is not None:
            yield node.right

    def num_children(self, node):
        count = int(node.left is not None) + int(node.right is not None)
        return count

    def replace(self, node, el):
        node.element = el
        return node

    def delete(self, node):
        if self.num_children(node) == 2:
            raise ValueError("node has 2 children")
        child = node.left if node.left is None else node.right
        if child is not None:
            child.parent = node.parent
        if self.is_root(node):
            self.root = child
        else:
            parent = node.parent
            if node is parent.left:
                parent.left = child
            else:
                parent.right = child
        self.size -= 1
        el = node.element
        node = None
        return el

    def attach(self, node, t1, t2):
        if not self.is_leaf(node):
            raise ValueError("Too many children")
        self.size += len(t1) + len(t2)
        if not t1.is_empty():
            t1.root.parent = node
            node.left = t1.root
            t1.root = None
            t1.size = 0
        if not t2.is_empty():
            t2.root.parent = node
            node.right = t2.root
            t2.root = None
            t2.size = 0

    def swap(self, n1, n2):

        if self.get_sibling(n1) is not n2:
            if (left1 := n1.left) is not None:
                left1.parent = n2
            if (right1 := n1.right) is not None:
                right1.parent = n2

            if (left2 := n2.left) is not None:
                left2.parent = n1
            if (right2 := n2.right) is not None:
                right2.parent = n1

        if n1 == n1.parent.left:
            n1.parent.left = n2
        else:
            n1.parent.right = n2

        if n2 == n2.parent.left:
            n2.parent.left = n1
        else:
            n2.parent.right = n1

        left, right = n1.left, n1.right
        n1.left, n1.right = n2.left, n2.right
        n2.left, n2.right = left, right
