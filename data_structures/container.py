class Container:

    def __init__(self, data=None):
        self.data = [] if data is None else data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, item, value):
        self.data[item] = value

    def __iter__(self):
        return iter(self.data)

    def append(self, value):
        self.data.append(value)

    def pop(self):
        return self.data.pop()

    def insert(self, index, value):
        self.data.insert(index, value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.data})"
