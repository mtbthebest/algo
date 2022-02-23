from math import log2, ceil
from data_structures import LinkedQueue
from collections import defaultdict, OrderedDict
import random
import copy
from functools import reduce


class EmptyError(Exception):
    ...


class Vertex:

    def __init__(self, value, **kwargs):
        self.value = value
        self.kwargs = kwargs

    @property
    def v(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value})"


class LVertex(Vertex):

    def __init__(self, value, **kwargs):
        super().__init__(value, **kwargs)

    def __index__(self):
        return self.value


class Edge:

    def __init__(self, head, tail, weight=None):
        self.head = head
        self.tail = tail
        self.weight = weight

    def __getitem__(self, item):
        assert item in [0, 1]
        return self.head if item == 0 else self.tail

    def __iter__(self):
        return iter([self.head, self.tail])

    def __hash__(self):
        return hash((self.head, self.tail))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.head}, {self.tail})"


class Path:

    def __init__(self, vertices):
        if len(vertices) < 2:
            raise EmptyError("Empty Path is not allowed")

        self.vertices = vertices
        self.start, self.end = self.vertices[0], self.vertices[-1]

    def is_cyclic(self):
        return isinstance(self.start, type(self.end)) and self.start is self.end

    def is_self_loop(self):
        return self.is_cyclic() and len(self.vertices) == 2

    def length(self):
        return len(self.vertices) - 1

    def __repr__(self):
        return f"{self.__class__.__name__}({(v.value for v in self.vertices)})"


class Graph:

    def __init__(self):
        pass

    @property
    def vertices(self):
        for e in self.edges:
            print(e)
            yield from e

    @property
    def edges(self):
        return iter(self)

    def __iter__(self):
        raise NotImplementedError

    def adjacent(self, vertex):
        raise NotImplementedError

    def is_adjacent(self, u, v):
        return u in self.adjacent(v)

    def get_vertex_degree(self, vertex):
        pass

    def insert_edge(self, edge):
        pass

    def insert_vertex(self, vertex):
        pass

    def remove_edge(self, edge):
        ...

    def remove_vertex(self, vertex):
        pass


class LinkedGraph(Graph):
    def __init__(self):
        super(LinkedGraph, self).__init__()
        self.data = []
        self.size = len(self.data)

    def __iter__(self):
        for v in self.edges:
            yield v

    @property
    def edges(self):
        for i, v in enumerate(self.data):
            if v is not None:
                adj = self.adjacent(v)
                for u in adj:
                    if i <= u.value:
                        yield Vertex(i), u

    def adjacent(self, vertex):
        adj = []
        h = vertex.head
        while h:
            adj.append(h.element)
            h = h.next
        return adj

    @property
    def vertices(self):
        _vertices = set()
        for v in self.data:
            if v is not None:
                for u in self.adjacent(v):
                    _vertices.add(u)

        return list(set(_vertices))

    def insert_edge(self, edge):
        head, tail = map(lambda vertex: vertex.value, edge)
        if (val := max(head, tail)) >= self.size:
            power = ceil(log2(val))
            new_size = 2 ** power if val < 2 ** power else 2 ** (power + 1)
            self.resize(new_size)
            self.size = new_size

        if self.data[head] is None:
            self.data[head] = LinkedQueue()
        if self.data[tail] is None:
            self.data[tail] = LinkedQueue()
        self.data[head].enqueue(edge.tail)
        self.data[tail].enqueue(edge.head)

    def resize(self, cap):
        self.data = self.data + [None] * (cap - self.size)

    def remove_edge(self, edge):
        head, tail = edge
        for (u, v) in ([head, tail], [tail, head]):
            qhead = self.data[u.value]
            vertices = []
            while (prev := qhead.dequeue()) != v:
                vertices.append(prev)
            for vertex in vertices:
                self.data[u.value].push(vertex)
            if self.data[u.value].size == 0:
                self.data[u.value] = None

    def __repr__(self):
        arrow = "->"
        space = self.size // 10 + 1
        for i in range(self.size):
            print(f"{i: >{space}}", end=" ")
            if self.data[i] is not None:
                h = self.data[i].head
                qval = ''
                while h:
                    qval += str(h.element.value) + arrow
                    h = h.next
                qval = qval[:qval.rfind(arrow)]
                print(qval)
            print()
        return ""


class MatrixGraph(Graph):
    CAP = 2

    def __init__(self):
        super(Graph, self).__init__()
        self.size = self.CAP
        self.data = [[0] * self.size for _ in range(self.size)]
        self._edges = []

    @property
    def edges(self):
        return self._edges

    def __iter__(self):
        for v in self.edges:
            yield v

    def insert_edge(self, edge):
        head, tail = edge
        self._edges.append(edge)
        head, tail = LVertex(head.value), LVertex(tail.value)
        if (val := max(head.value, tail.value)) >= self.size:
            power = ceil(log2(val))
            new_size = 2 ** power if val < 2 ** power else 2 ** (power + 1)
            self.resize(new_size)
            self.size = new_size
        self.data[head][tail] = 1
        self.data[tail][head] = 1

    def remove_edge(self, e):
        self._edges.remove(e)
        h, t = self._get_vertices(e)
        self.data[h][t] = 0
        self.data[t][h] = 0

    def _get_vertices(self, edge):
        head, tail = edge
        head, tail = LVertex(head.value), LVertex(tail.value)
        return head, tail

    def resize(self, cap):
        for i in range(self.size):
            self.data[i] += [0] * (cap - self.size)
        self.data += [[0] * cap for _ in range(cap - self.size)]

    def __repr__(self):
        sp = ' '
        space = self.size // 10 + 1
        print(f"{sp: >{space}}", end=" ")
        for i in range(self.size):
            print(f"{i: >{space}}", end=" ")
        print()
        for i in range(self.size):
            print(f"{i: >{space}}", end=" ")
            for j in range(self.size):
                print(f"{self.data[i][j]: >{space}}", end=" ")
            print()

        return ""


class MapGraph(Graph):

    def __init__(self, directed=False):
        super().__init__()
        self.data = defaultdict(OrderedDict)
        self.num_edges = 0
        self.directed = directed

    def __iter__(self):
        return self.edges

    def insert_edge(self, edge):
        head, tail = edge
        self.data[head][tail] = edge
        if not self.directed:
            self.data[tail][head] = edge
        self.num_edges += 1

    def remove_edge(self, edge):
        head, tail = edge
        del self.data[head][tail]
        if not self.directed:
            del self.data[tail][head]
        self.num_edges -= 1

    def adjacent(self, vertex):
        for edge in sorted(self.data[vertex].values(), key=lambda e: (e[0].v, e[1].v)):
            yield edge[0] if edge[0] != vertex else edge[1]

    @property
    def vertices(self):
        for vertex in set(reduce(lambda head, tail: tuple(head) + tuple(tail),
                                 map(lambda edge: (edge[0], edge[1]), self.edges))):
            yield vertex

    @property
    def edges(self):
        for edge in sorted(set(edge for _, vl in self.data.items() for _, edge in vl.items()),
                           key=lambda e: (e[0].v, e[1].v)):
            yield edge

    def __repr__(self):
        return "\n".join(map(lambda edge: str(edge), self.edges))

    def generate_graph(self, max_vertices, max_edges=1, ):
        p = 2 * max_edges / (max_vertices * (max_vertices - 1))
        for i in range(max_vertices):
            for j in range(i):
                if random.random() < p:
                    self.insert_edge(Edge(Vertex(i), Vertex(j)))

    def get_edge(self, head, tail):
        return self.data[head].get(tail)

    def count_edges(self):
        return self.num_edges

    def count_vertices(self):
        return len(list(self.vertices))

    def indegree(self, vertex):
        return sum(map(lambda e: e[1] == vertex, self.edges))

    def outdegree(self, vertex):
        return len(self.data.get(vertex)) if self.data.get(vertex) is not None else 0

    def __deepcopy__(self, memodict):
        obj = MapGraph(directed=self.directed)
        memodict[id(obj)] = obj
        for edge in self.edges:
            head, tail = edge
            if id(head) not in memodict:
                memodict[id(head)] = copy.deepcopy(head)
            if id(tail) not in memodict:
                memodict[id(tail)] = copy.deepcopy(tail)
            head, tail = memodict[id(head)], memodict[id(tail)]
            obj.insert_edge(Edge(head, tail, weight=edge.weight))
        return obj

    def __copy__(self):
        obj = MapGraph(self.directed)
        obj.__dict__.update(self.__dict__)
        return obj

    def print_edge(self, edge):
        head, tail = edge.head, edge.tail
        print(f"{head.value}-{tail.value}")

    def reverse(self):
        g = self.__class__(self.directed)
        for edge in self.edges:
            head, tail = edge
            new_edge = copy.copy(edge)
            new_edge.head, new_edge.tail = tail, head
            g.insert_edge(new_edge)
        return g


class DirectedMapGraph(MapGraph):

    def __init__(self):
        super(DirectedMapGraph, self).__init__()
        self.directed = True
