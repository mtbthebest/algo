class UF:
    class Item:
        def __init__(self, value, parent=None):
            self.value = value
            self.parent = self if parent is None else parent

    def __init__(self, nodes=None):
        nodes = list(nodes) if nodes else []
        self.items = []
        for node in nodes:
            self.items.append(self.Item(node))
        self._count = len(self.items)

    @property
    def count(self):
        return self._count

    def union(self, p, q):
        pid, qid = self.find(p), self.find(q)
        if pid == qid:
            return
        pid.parent = qid
        return True

    def find(self, p):
        item = filter(lambda it: it.value == p, self.items)
        item = list(item)
        if not item or len(item) > 1:
            raise ValueError
        item = item[0]

        while item.parent != item:
            item = item.parent
        return item
