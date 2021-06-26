from abc import ABC
from collections import MutableMapping
from random import randrange
from copy import deepcopy


class MapBase(MutableMapping):
    class Item:
        __slots__ = ("key", "value")

        def __init__(self, k, v):
            self.key = k
            self.value = v

        def __eq__(self, other):
            return self.key == other.key

        def __ne__(self, other):
            return not (self == other)

        def __lt__(self, other):
            return self.key < other.key


class TableMap(MapBase):

    def __init__(self):
        self.data = []

    def __getitem__(self, k):
        for item in self.data:
            if item.key == k:
                return item.value
        raise KeyError(f"Key {k} was not found")

    def __setitem__(self, key, value):
        for item in self.data:
            if item.key == key:
                item.value = value
                return
        else:
            self.data.append(self.Item(key, value))

    def __iter__(self):
        for item in self.data:
            yield item.key

    def __len__(self):
        return len(self.data)

    def __delitem__(self, k):
        for i, item in enumerate(self.data):
            if item.key == k:
                self.data[i], self.data[-1] = self.data[-1], self.data[i]
                self.data.pop()
                return
        else:
            raise KeyError(f"Key {k} was not found")


class HashMapBase(MapBase):

    def __init__(self, cap=11, p=109345121):
        self.table = [None] * cap
        self.n = 0
        self.prime = p
        self.scale = 1 + randrange(p - 1)
        self.shift = randrange(p)

    def hash_function(self, k):
        """h_{ab} universal hash function"""
        return (hash(k) * self.scale + self.shift) % self.prime % len(self.table)

    def __len__(self):
        return self.n

    def bucket_getitem(self, j, k):
        raise NotImplementedError

    def bucket_setitem(self, j, k, v):
        raise NotImplementedError

    def bucket_delitem(self, j, k):
        raise NotImplementedError

    def __getitem__(self, k):
        j = self.hash_function(k)
        return self.bucket_getitem(j, k)

    def __setitem__(self, k, v):
        j = self.hash_function(k)
        self.bucket_setitem(j, k, v)
        # Implement the sizing of the bucket
        if self.n > len(self.table) // 2:  # Load Factor
            self.resize(2 * len(self.table) - 1)

    def __delitem__(self, k):
        j = self.hash_function(k)
        self.bucket_delitem(j, k)
        self.n -= 1

    def resize(self, size):
        table = list(self.items())
        self.table = [None] * size
        for (k, v) in table:
            # k = self.hash_function(k) # To consider
            self.table[k] = v

    def __iter__(self):
        raise NotImplementedError


class ChainHashMap(HashMapBase):
    # Chain depends on TableMap

    def bucket_getitem(self, j, k):
        bucket = self.table[j]
        if bucket is None:
            raise KeyError

        return bucket[k]

    def bucket_setitem(self, j, k, v):
        bucket = self.table[j]
        if bucket is None:
            self.table[j] = TableMap()
        size = len(self.table[j])
        self.table[j][k] = v
        if len(self.table[j]) > size:
            self.n += 1

    def bucket_delitem(self, j, k):
        bucket = self.table[j]
        if bucket is None:
            raise KeyError
        del bucket[k]

        if len(bucket) == 0:
            self.table[j] = None

    def __iter__(self):
        for bucket in self.table:
            if bucket is not None:
                for k in bucket:
                    yield k


class ProbeHashMap(HashMapBase):
    # """h(k) = h'(k) +i """
    sentinel = object()

    def is_available(self, j):
        return self.table[j] is None or self.table[j] is self.sentinel

    #
    def find_slot(self, j, k):
        """Search for key k in bucket at index j.
            Return (success, index) tuple, described as follows:
            If match was found, success is True and index denotes its location.
            If no match found, success is False and index denotes first available slot.
        """

        firstAvail = None
        while True:
            if self.is_available(j):
                if firstAvail is None:
                    firstAvail = j
                if self.table[j] is None:
                    return False, firstAvail
            elif k == self.table[j].key:
                return True, j
            j = (j + 1) % len(self.table) # Linear probing Quadratic probing: (j+1) ** 2 , double hashing h(k)+i h'(h)

    def bucket_getitem(self, j, k):
        found, s = self.find_slot(j, k)
        if not found:
            raise KeyError
        return self.table[s].value

    def bucket_setitem(self, j, k, v):
        found, s = self.find_slot(j, k)
        if found:
            self.table[s].value = v
        else:
            self.table[s] = self.Item(k, v)
            self.n += 1

    def bucket_delitem(self, j, k):
        found, s = self.find_slot(j, k)
        if not found:
            raise KeyError
        self.table[s] = self.sentinel

    def __iter__(self):
        for j in range(len(self.table)):
            if not self.is_available(j):
                yield self.table[j].key
