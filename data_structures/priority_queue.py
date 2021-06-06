class PriorityQueueBase:
    class Item:
        __slots__ = ("key", "value")

        def __init__(self, k, v):
            self.key = k
            self.value = v

        def __lt__(self, other):
            return self.key < other.key

        def __repr__(self):
            return f"Item(key={self.key}, value={self.value})"

    def __len__(self):
        raise NotImplementedError

    def is_empty(self):
        return len(self) == 0


class UnSortedPriorityQueue(PriorityQueueBase):
    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def find_min(self):
        if self.is_empty():
            raise ValueError
        smallest = self._data[0]

        for i in range(len(self._data)):
            if self._data[i] < smallest:
                smallest = self._data[i]
        return smallest

    def add(self, key, value):
        self._data.append(self.Item(key, value))

    def min(self):
        item = self.find_min()
        return item.key, item.value

    def remove_min(self):
        item = self.find_min()
        self._data.remove(item)

        return item.key, item.value


class SortedPriorityQueue(PriorityQueueBase):

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def add(self, key, value):
        item = self.Item(key, value)
        if self.is_empty():
            self._data.append(item)
        else:
            for i in range(len(self._data)):
                if item > self._data[i]:
                    self._data.insert(i, item)
                    break
            else:
                self._data.append(item)

    def remove_min(self):
        if self.is_empty():
            raise ValueError
        item = self._data.pop()
        return item.key, item.value

    def min(self):
        if self.is_empty():
            raise ValueError
        item = self._data[-1]
        return item.key, item.value

    def __repr__(self):
        return repr(self._data)
