import numpy as np

int = np.int64


class Bitset:
    def __init__(self, m, n):
        self.inverted = False
        self.rows = m
        self.columns = n
        if m > n:
            self.inverted = True
        if self.inverted:
            n, m = m, n
        k = int(np.ceil(n / 64))
        self.table = np.zeros((m, k), np.int64)

    def __getitem__(self, item):
        if not isinstance(item, tuple) or len(item) < 2: raise ValueError()

        if item[0] >= self.rows or item[1] >= self.columns or item[0] < 0 or item[1] < 0:
            raise IndexError("Index out of bounds")

        if self.inverted:
            item = item[1], item[0]

        pos, offset = int(item[1] / 64), int(item[1] % 64)
        return (self.table[item[0]][pos] & (1 << offset)) != 0

    def __setitem__(self, item, value):
        if item[0] >= self.rows or item[1] >= self.columns or item[0] < 0 or item[1] < 0:
            raise IndexError("Index out of bounds")
        if self.inverted:
            item = item[1], item[0]

        pos, offset = int(item[1] / 64), int(item[1] % 64)
        if value == True:
            self.table[item[0]][pos] |= (1 << offset)
        elif self.table[item[0]][pos] & (1 << offset) != 0:
            self.table[item[0]][pos] ^= (1 << offset)

    def print(self):
        print(self)

    def __str__(self):
        arr = []
        for i in range(self.rows):
            l = []
            for j in range(self.columns):
                l.append(self[i, j])
            arr.append(l)
        p = '\n'.join(''.join(map(lambda x: 'X' if x else '.', l)) for l in arr)
        return p

    def __eq__(self, other):
        if not isinstance(other, Bitset):
            return False
        if self.rows != other.rows or self.columns != other.columns: return false
        return all((self.table == other.table).flatten())


if __name__ == "__main__":
    a = Bitset(200, 5)
    print(a.rows, a.columns)
    a[2, 2] = True
    a[0, 1] = True
    print(a[2, 2], a[0, 1], a[3, 3])
    a[0, 1] = False
    print(a[0, 1])
    a[2, 0] = True
    a[150, 4] = True
    print(a.table)
