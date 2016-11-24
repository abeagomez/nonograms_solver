import numpy as np


# region Generate all solutions

def matches(expanded_solution, constraints):
    """
    solution is a tuple of spaces, the output of solve1
    constraints is a tuple of values from 1, 0 and -1, that
    mean:
         0 -> OFF
         1 -> ON
        -1 -> not constrained
    """
    for s, c in zip(expanded_solution, constraints):
        if c == -1:
            continue
        if c != s:
            return False
    return True


def expand_solution(solution, width, pattern):
    """
    expands a solution to a tuple of 1 (ON) and 0 (OFF)
    """
    r = []
    for s, p in zip(solution, pattern):
        r.extend([0] * s)
        r.extend([1] * p)
    r.extend([0] * (width - sum(solution) - sum(pattern)))
    return tuple(r)


def solutions(width, pattern, constraints=None):
    """
    @width: int
    @pattern: sequence of ints
    @constraints: optional list of length width containing 1,0,-1 as elements

    Does the same as solve1, but takes constraints
    in consideration to be faster than solve1 + matches
    """

    if len(pattern) == 0:
        return tuple()

    if constraints is None:
        constraints = [-1] * width

    p = pattern[0]

    # the first gap can go from 0 to the following, inclusive
    maxgap = width - sum(pattern[1:]) - (len(pattern) - 1) - p

    for gap in range(maxgap + 1):
        e = expand_solution((gap,), gap + p + 1, (p,))
        if not matches(e, constraints[:gap + p + 1]):
            continue
        # if len(pattern) == 1:
        # You have to check that there are no fixed boxes after the sole constrain.
        if len(pattern) == 1 and np.all(constraints[gap + p + 1:] < 1):
            yield (gap,)
            continue
        subwidth = width - gap - p - 1
        subpattern = pattern[1:]
        subconstraints = constraints[-subwidth:]
        for s in solutions(subwidth, subpattern, subconstraints):
            yield (gap, s[0] + 1) + s[1:]


# endregion

class Problem:
    def __init__(self, column_restrictions, row_restrictions):
        self.width = len(column_restrictions)
        self.height = len(row_restrictions)
        self.columns = column_restrictions
        self.rows = row_restrictions
        self.board = -np.ones((self.height, self.width), dtype=np.int8)
        self.sol_row = None
        self.sol_col = None

    # region Line set and get

    def line(self, l):
        return self.row(l[o]) if l[1] == 'R' else self.column(l[0])

    def row(self, i):
        return self.board[i]

    def column(self, i):
        return self.board.T[i]

    def set_line(self, l, value):
        if l[1] == 'R':
            self.set_row(i, value)
        else:
            self.set_column(i, value)

    def set_row(self, i, value):
        self.board[i] = value[:]

    def set_column(self, i, value):
        self.board.T[i] = value[:]

    def copy(self):
        p = Problem(self.columns, self.rows)
        p.board = self.board.copy()
        return p

    # endregion

    def fix_all(self):
        sol_row = [None for i in range(self.height)]
        sol_col = [None for i in range(self.width)]
        while True:
            changed = False
            for i in range(self.width):
                pattern = self.columns[i]
                constrains = self.column(i)
                sol_col[i] = []
                inv = None
                for sol in solutions(self.height, pattern, constrains):
                    e = np.array(expand_solution(sol, self.height, pattern))
                    sol_col[i].append(e)
                    e = e.copy()
                    if inv is None:
                        inv = e
                    else:
                        different = np.logical_not(inv == e)
                        inv[different] = -np.ones(len(inv[different]))
                    if inv is not None and np.all(inv == -1):
                        break
                if np.any(inv != constrains):
                    self.set_column(i, inv)
                    changed = True

            for i in range(self.height):
                pattern = self.rows[i]
                constrains = self.row(i)
                sol_row[i] = []
                inv = None
                for sol in solutions(self.width, pattern, constrains):
                    e = np.array(expand_solution(sol, self.width, pattern))
                    sol_row[i].append(e)
                    e = e.copy()
                    if inv is None:
                        inv = e
                    else:
                        different = np.logical_not(inv == e)
                        inv[different] = -np.ones(len(inv[different]))
                    if inv is not None and np.all(inv == -1):
                        break
                if np.any(constrains != inv):
                    self.set_row(i, inv)
                    changed = True

            if not changed: break
        self.sol_row, self.sol_col = sol_row, sol_col
        return sol_col, sol_row

    def solve(self):
        self.fix_all()
        sizes_col = [x for x in map(len, self.sol_col)]
        sizes_row = [x for x in map(len, self.sol_row)]
        min_col = min(sizes_col)
        min_row = min(sizes_row)

        if min_col == 0 or min_row == 0:
            return False

        if max(sizes_col) == 1 and max(sizes_row) == 1:
            return True

        min_col = min([(x, i) for i, x in enumerate(sizes_col) if x > 1])
        min_row = min([(x, i) for i, x in enumerate(sizes_row) if x > 1])

        if min_col < min_row:
            idx = min_col[1]
            for sol in self.sol_col[idx]:
                p = self.copy()
                p.set_column(idx, sol)
                if p.solve():
                    return True

        else:
            idx = min_row[1]
            for sol in self.sol_row[idx]:
                p = self.copy()
                p.set_row(idx, sol)
                if p.solve():
                    return True


if __name__ == '__main__':
    from pprint import pprint
    import time

    t = time.time()
    p = Problem([[2, 1], [2, 1, 1], [1, 1, 1, 1], [2, 1], [1, 1, 1], [1, 1, 1, 1], [3], [3, 2, 1], [1, 1, 3, 1],
                 [1, 1, 1, 1], [1, 2, 1, 1, 1], [1, 1, 1, 1], [1, 2, 1], [1], [1, 4, 1]],
                [[1, 2, 1], [1, 3, 1], [1, 1, 3], [1, 1, 1], [1, 1], [1, 1], [1, 2, 1, 1, 1], [2, 3, 3, 1, 1],
                 [1, 1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1], [1, 2], [1, 1], [1, 1, 1]])
    print(p.solve())
    print(time.time() - t)
