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
        yield tuple()
        return

    if constraints is None:
        constraints = [-1] * width

    p = pattern[0]

    # the first gap can go from 0 to the following, inclusive
    maxgap = width - sum(pattern[1:]) - (len(pattern) - 1) - p

    for gap in range(maxgap + 1):
        # constraint width
        cw = (gap + p + 1) if len(pattern) > 1 else width
        e = expand_solution((gap,), cw, (p,))
        if not matches(e, constraints[:cw]):
            continue
        if len(pattern) == 1:
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
        self.board = [[-1] * self.width for i in range(self.height)]
        self.sol_row = None
        self.sol_col = None

    # region Line set and get

    def line(self, l):
        return self.row(l[o]) if l[1] == 'R' else self.column(l[0])

    def row(self, i):
        return self.board[i]

    def column(self, i):
        return [self.board[x][i] for x in range(self.height)]

    def set_line(self, l, value):
        if l[1] == 'R':
            self.set_row(i, value)
        else:
            self.set_column(i, value)

    def set_row(self, i, value):
        self.board[i] = list(value[:])

    def set_column(self, i, value):
        for x in range(self.height):
            self.board[x][i] = value[x]

    def copy(self):
        p = Problem(self.columns, self.rows)
        for i in range(self.height):
            p.board[i] = self.board[i][:]
        return p

    # endregion

    def fix_all(self):
        while True:
            sol_col = [0] * self.width
            sol_row = [0] * self.height
            changed = False
            for i in range(self.width):
                pattern = self.columns[i]
                constrains = self.column(i)
                inv = None
                count = 0
                for sol in solutions(self.height, pattern, constrains):
                    e = list(expand_solution(sol, self.height, pattern))
                    if inv is None:
                        inv = e
                    for y, ex in enumerate(e):
                        if inv[y] != ex:
                            inv[y] = -1
                    count += 1
                sol_col[i] = count
                if inv is not None and self.column(i) != inv:
                    self.set_column(i, inv)
                    changed = True

            for i in range(self.height):
                pattern = self.rows[i]
                constrains = self.row(i)
                inv = None
                count = 0
                for sol in solutions(self.width, pattern, constrains):
                    e = list(expand_solution(sol, self.width, pattern))
                    if inv is None:
                        inv = e
                    for y, ex in enumerate(e):
                        if inv[y] != ex:
                            inv[y] = -1
                    count += 1
                sol_row[i] = count
                if inv is not None and self.row(i) != inv:
                    self.set_row(i, inv)
                    changed = True
            if not changed: break
        return sol_col, sol_row

    def solve(self):
        sizes_col, sizes_row = self.fix_all()
        min_col = min(sizes_col)
        min_row = min(sizes_row)

        if min_col == 0 or min_row == 0:
            return None

        if max(sizes_col) == 1 and max(sizes_row) == 1:
            return self.board

        min_col, x = min([(x, i) for i, x in enumerate(sizes_col) if x > 1])
        min_row, y = min([(x, i) for i, x in enumerate(sizes_row) if x > 1])

        if min_col < min_row:
            for sol in solutions(self.height, self.columns[x], self.column(x)):
                p = self.copy()
                p.set_column(x, expand_solution(sol, self.height, self.columns[x]))
                r = p.solve()
                if r: return r

        else:
            for sol in solutions(self.width, self.rows[y], self.row(y)):
                p = self.copy()
                p.set_row(y, expand_solution(sol, self.width, self.rows[y]))
                r = p.solve()
                if r: return r


def fdfs(width: int, col_rest: list, row_rest: list):
    p = Problem(col_rest, row_rest)
    return p.solve()


if __name__ == '__main__':
    from pprint import pprint
    import time

    t = time.time()
    p = Problem(
        [[1, 5, 2], [1, 1, 2], [1, 1, 2, 1, 2], [2, 2], [2, 1, 1, 1], [1, 1, 1], [1, 1], [1, 1, 1], [2, 3, 1, 1],
         [1, 2, 3, 1, 1], [1, 3, 1, 1], [2, 1, 1, 1], [1, 1, 1, 2, 1], [1, 1, 1, 2, 1], [2, 1]],
        [[1, 2, 1, 1], [1, 1, 4], [2, 1], [1, 1, 1, 1, 2], [1, 3, 1, 1], [1, 2], [1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 2], [1, 1, 2], [1, 2, 1, 1], [3, 1, 4], [1, 4, 1], [3], [3, 1, 1], [1, 2, 1]]
    )
    pprint(p.solve())
    print(time.time() - t)
