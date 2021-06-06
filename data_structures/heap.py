from . import PriorityQueueBase
from math import floor


class HeapPriorityQueue(PriorityQueueBase):
    def __init__(self, contents=()):
        self._data = [self.Item(k, v) for k, v in contents]
        self._size = None
        if len(self) > 1:
            self.heapify()

    def __len__(self):
        return self.size or len(self._data)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, s):
        self._size = s

    def is_empty(self):
        return len(self) == 0

    def parent(self, i):
        return floor((i - 1) / 2)

    def left(self, i):
        return 2 * i + 1

    def right(self, i):
        return 2 * i + 2

    def has_left(self, i):
        return self.left(i) < len(self)

    def has_right(self, i):
        return self.right(i) < len(self)

    def has_parent(self, i):
        return i > 0

    def swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def upheap(self, i):
        while (parent := self.parent(i)) and parent >= 0 and self._data[parent] > self._data[i]:
            self.swap(parent, i)
            i = parent

    def downheap(self, i):
        if self.has_left(i):
            left = self.left(i)
            small_child = left
            if self.has_right(i):
                right = self.right(i)
                if self._data[right] < self._data[left]:
                    small_child = right

            if self._data[small_child] < self._data[i]:
                self.swap(small_child, i)
                self.downheap(small_child)

    def add(self, key, value):
        self._data.append(self.Item(key, value))
        self.upheap(len(self) - 1)

    def min(self):
        if self.is_empty():
            raise ValueError
        item = self._data[0]
        return item.key, item.value

    def remove_min(self):
        if self.is_empty():
            raise ValueError
        self.swap(0, len(self) - 1)
        item = self._data.pop()
        self.downheap(0)
        return item.key, item.value

    def heapify(self):
        start = self.parent(len(self) - 1)
        for j in range(start, -1, -1):
            self.downheap(j)

    def sort(self):
        if self.is_empty():
            raise ValueError

        def cmp(s, other):
            return s.key > other.key

        old_cmp = self.Item.__lt__
        self.Item.__lt__ = cmp

        self.size = len(self)
        self.heapify()
        for i in range(self.size - 1, 0, -1):
            self.swap(0, i)
            self.size -= 1
            self.downheap(0)

        self.Item.__lt__ = old_cmp

        self.size = len(self._data)

    def __repr__(self):
        return repr([item.key for item in self._data])

    @classmethod
    def register_cmp_function(cls, cmp):
        cls.Item.__lt__ = cmp