from numbers import Number


class Vector:

    def __init__(self, d):
        self._d = d
        self._coords = [0] * self.d

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, value):
        if not isinstance(value, Number):
            raise TypeError(f"d must be an integer")
        self._d = value

    def __len__(self):
        return self.d

    def __repr__(self):
        return f"Vector({','.join(map(lambda c: str(c), self._coords))})"

    def __getitem__(self, item):
        return self._coords[item]

    def __setitem__(self, key, value):
        self._coords[key] = value

    def __add__(self, other):
        if len(self._coords) != len(other._coords):
            raise ValueError("Dimension do not match")
        v = Vector(self.d)

        for i in range(self.d):
            v[i] = self[i] + other[i]

        return v

    def __radd__(self, other):
        return self + other


    def __iadd__(self, other):
        if len(self._coords) != len(other._coords):
            raise ValueError("Dimension do not match")
        for i in range(self.d):
            self[i] += other[i]

        return self

    def __sub__(self, other):
        if len(self._coords) != len(other._coords):
            raise ValueError("Dimension do not match")
        v = Vector(self.d)

        for i in range(self.d):
            v[i] = self[i] - other[i]

        return v

    def __rsub__(self, other):
        return self - other

    def __mul__(self, other):
        print(other, "yr ")
        if isinstance(other, Vector):
            return self.dot_product(other)
        elif isinstance(other, Number):
            v = Vector(self.d)
            for i in range(self.d):
                v[i] = self[i] * other
            return v
        else:
            raise TypeError("Operations not defined")

    def __rmul__(self, other):
        print(other, "rmul ")
        return self * other

    def __eq__(self, other):
        return other._coords == self._coords

    def __pos__(self):
        return self

    def __abs__(self):
        v = Vector(self.d)
        for i in range(self.d):
            v[i] = abs(self[i])
        return v

    def __neg__(self):
        for i in range(self.d):
            self[i] = -self[i]
        return self

    def __ne__(self, other):
        return not self == other

    def dot_product(self, other):
        """Returns dot product"""
        if len(self._coords) != len(other._coords):
            raise ValueError("Dimension do not match")
        return sum((self[i] * other[i]) for i in range(self.d))


if __name__ == '__main__':
    v = Vector(2)
    v[0] = 4
    u = Vector(2)
    u[0] = -4
    print(v)
    print(v[0])
    w = u + v
    print(+v)
    print(w, u, v, u == v, +u == v)
    print(u != v, +u != v, u is v, +u is v)

    z = u - v
    print(f"z:{z}")
    z2 = u * v, u * 2
    print(z2)
    z3 = u*2
    z3 += z3
    print(z3)
    print(abs(z3))
