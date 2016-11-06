import numpy as np


class Bitset:
    """
    Efficient implementation of a binary matrix.
    """

    def __init__(self, m, n):
        self.inverted = False
        self.rows = m
        self.columns = n
        if m > n:
            self.inverted = True
        if self.inverted:
            n, m = m, n
        self.table = np.zeros((m,), int)

    def __getitem__(self, item):
        if not isinstance(item, tuple) or len(item) < 2: raise ValueError()

        if item[0] >= self.rows or item[1] >= self.columns or item[0] < 0 or item[1] < 0:
            raise IndexError("Index out of bounds")

        if self.inverted:
            item = item[1], item[0]

        return bool(self.table[item[0]] & 1 << item[1])

        pos, offset = int(item[1] / 64), int(item[1] % 64)
        return (self.table[item[0]][pos] & (1 << offset)) != 0

    def __setitem__(self, item, value):
        if item[0] >= self.rows or item[1] >= self.columns or item[0] < 0 or item[1] < 0:
            raise IndexError("Index out of bounds")
        if self.inverted:
            item = item[1], item[0]
        offset = int(item[1] % 64)
        mask = 1 << offset
        if value == True:
            self.table[item[0]] |= mask
        elif bool(self.table[item[0]] & mask):
            self.table[item[0]] ^= mask

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
        if self.rows != other.rows or self.columns != other.columns: return False
        return all((self.table == other.table).flatten())

    def save(self, filename: str):
        with open(filename, 'w') as file:
            file.write("{} {}\n".format(self.rows, self.columns))
            file.write(str(self))

    @staticmethod
    def load(filename: str):
        with open(filename) as file:
            r, c = [int(x) for x in file.readline().strip().split()]
            b = Bitset(r, c)
            ctr = 0
            while ctr < r:
                l = file.readline(c + 1).strip()
                start = 0
                while l.find('X', start) >= 0:
                    pos = l.index('X', start)
                    b[ctr, pos] = True
                    start = pos + 1
                ctr += 1
            return b


if __name__ == "__main__":
    a = Bitset(6, 5)
    print(a.rows, a.columns)
    print(a[0, 0])
    a[2, 2] = True
    a[0, 1] = True
    print(a[2, 2], a[0, 1], a[3, 3])
    a[0, 1] = False
    print(a[0, 1])
    a[2, 0] = True
    a.save('test_board')
    print(a)
    b = Bitset.load('test_board')
    print('-----------------', b, sep='\n')
