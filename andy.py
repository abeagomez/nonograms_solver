#!/usr/bin/env python3

"This module does something"

from itertools import combinations_with_replacement
import sys


def solve1(width, pattern):
    """
    This yields a tuple for each possible layout of
    pattern inside the row. The tuple elements are the
    gaps before each block in pattern.
    The tuple doesn't include the last gap, since that's
    just: width - sum(sol) - sum(pattern)
    """
    spaces = width - (sum(pattern) + len(pattern) - 1)
    for sol in combinations_with_replacement(range(spaces + 1), len(pattern)):
        sol = sol[0:1] + tuple((sol[i] - sol[i - 1] + 1) for i in range(1, len(sol)))
        yield sol


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


def solve2(width, pattern, constraints=None):
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
        for s in solve2(subwidth, subpattern, subconstraints):
            yield (gap, s[0] + 1) + s[1:]


def invariants(width, pattern, constraints=None):
    "compute invariants"
    invs = []
    for sol in solve2(width, pattern, constraints):
        exp = list(expand_solution(sol, width, pattern))
        if len(invs) == 0:
            invs = exp
        else:
            for i, e in enumerate(exp):
                if invs[i] != e:
                    invs[i] = -1
    return invs


def visual(constraints):
    "returns a visual representation of constraints"
    return "".join({
                       1: '\N{FULL BLOCK}\N{LEFT SEVEN EIGHTHS BLOCK}',
                       0: '__',
                       -1: '??'
                   }[x] for x in constraints)


class Board:
    """Board

    A board is actually a list of constraints.
    A cell with 1 or 0 is fixed. A cell with -1
    doesn't have a known value yet.
    """

    def __init__(self, patterns):
        self.col_patterns = patterns[0]
        self.row_patterns = patterns[1]
        self.width = len(patterns[0])
        self.height = len(patterns[1])
        self.rows = [None] * self.height
        for i in range(self.height):
            self.rows[i] = [-1] * self.width

            # print("rows:")
            # for y in range(self.height):
            #     n, c = invariants(self.width, self.row_patterns[y])
            #     print(n, self.row_patterns[y], visual(c))

            # print("cols:")
            # for x in range(self.height):
            #     n, c = invariants(self.width, self.col_patterns[x])
            #     print(n, self.col_patterns[x], visual(c))

            # print(self.row(0))

    def col(self, i):
        """a column"""
        return [self.rows[x][i] for x in range(self.height)]

    def row(self, i):
        """a row"""
        return self.rows[i]

    def replace_row(self, i, row):
        self.rows[i] = row

    def replace_col(self, i, col):
        for y in range(self.height):
            self.rows[y][i] = col[y]

    def copy(self):
        newboard = Board((self.col_patterns, self.row_patterns))
        for i in range(self.height):
            newboard.rows[i] = self.rows[i][:]
        return newboard

    def __str__(self):
        s = ""
        for y in range(self.height):
            s += visual(self.rows[y])
            s += "\n"
        return s

    def compute_invariants(self):
        while True:
            changed = False

            row_sols = [0] * self.height
            col_sols = [0] * self.width

            # rows
            for y in range(self.height):
                invs = None;
                count = 0
                for sol in solve2(self.width, self.row_patterns[y], self.row(y)):
                    count += 1
                    exp = list(expand_solution(sol, self.width, self.row_patterns[y]))
                    if invs == None:
                        invs = exp
                    for i, e in enumerate(exp):
                        if invs[i] != e:
                            invs[i] = -1
                if invs != None and self.row(y) != invs:
                    self.replace_row(y, invs)
                    changed = True
                row_sols[y] = count

            # columns
            for x in range(self.width):
                invs = None;
                count = 0
                for sol in solve2(self.height, self.col_patterns[x], self.col(x)):
                    count += 1
                    exp = list(expand_solution(sol, self.height, self.col_patterns[x]))
                    if invs == None:
                        invs = exp
                    for i, e in enumerate(exp):
                        if invs[i] != e:
                            invs[i] = -1
                if invs != None and self.col(x) != invs:
                    self.replace_col(x, invs)
                    changed = True
                col_sols[x] = count

            if not changed:
                break

        return row_sols, col_sols

    def solve(self, solved=lambda x: None, depth=0):
        row_sols, col_sols = self.compute_invariants()
        # if depth < 2:
        #     print("depth:", depth)
        #     print(self)
        #     print("row_sols:", row_sols)
        #     print("col_sols:", col_sols)

        if min(row_sols) == 0 or min(col_sols) == 0:
            return False

        if max(row_sols) == 1:
            print("solved")
            solved(self)
            return True

        min_row, y = min((a, b) for b, a in enumerate(row_sols) if a > 1)
        min_col, x = min((a, b) for b, a in enumerate(col_sols) if a > 1)

        if min_row < min_col:
            for sol in solve2(self.width, self.row_patterns[y], self.row(y)):
                b = self.copy()
                b.replace_row(y, expand_solution(sol, self.width, self.row_patterns[y]))
                if b.solve(solved, depth + 1):
                    return True
        else:
            for sol in solve2(self.height, self.col_patterns[x], self.col(x)):
                b = self.copy()
                b.replace_col(x, expand_solution(sol, self.height, self.col_patterns[x]))
                if b.solve(solved, depth + 1):
                    return True


if __name__ == "__main__":

    def draw(solution, width, pattern):
        "draws a solution"
        for s, p in zip(solution, pattern):
            print('__' * s, end="")
            print('\N{FULL BLOCK}\N{LEFT SEVEN EIGHTHS BLOCK}' * p, end="")
        print('__' * (width - sum(solution) - sum(pattern)))


    # width = int(sys.argv[1])
    # pattern = tuple(int(x) for x in sys.argv[2].split())
    # constraints = [-1] * width
    # try:
    #     for i, c in enumerate(sys.argv[3]):
    #         constraints[i] = {'1':1, '0':0, '?':-1}[c]
    # except:
    #     constraints = [-1] * width

    # for solution in solve1(width, pattern):
    #     e = expand_solution(solution, width, pattern)
    #     if matches(e, constraints):
    #         draw(solution, width, pattern)

    def parse(rows):
        "parses '1 1, 1 2 3' into [[1, 1], [1, 2, 3]]"
        rows = rows.split(",")
        rows = [[int(y) for y in x.strip().split()] for x in rows]
        return rows


    def parse_constraints(s, width):
        constraints = [-1] * width
        for i, c in enumerate(s):
            constraints[i] = {'1': 1, '0': 0, '?': -1, '.': 0, '\N{LEFT SEVEN EIGHTHS BLOCK}': 1}[c]
        return constraints


    # width = 15
    # pattern = (1, 1, 1, 2)
    # constraints = parse_constraints('????????010?', width)
    # for sol in solve2(width, pattern, constraints):
    #     draw(sol, width, pattern)

    # b = Board((
    #     parse("1 1 1, 1 1 1, 1 1 1, 1 1 1, 1 1 1, 1 1 1"),
    #     parse("1 1 1, 1 1 1, 1 1 1, 1 1 1, 1 1 1, 1 1 1")
    # ))
    # b.solve(print)

    # b = Board((
    #     parse("""1 1 1 1 1, 1 1 1, 1 1 1 1, 1 2, 1 1 1 1, 1 1 1, 1 1 1,
    #              3 1, 1 1, 1 2 6 1, 2 1, 2 3 1, 1 1, 1 1 3 1, 2 1 1"""),
    #     parse("""1 2, 1 1 2, 2 1 1 1 1, 3 1, 1 1 1 1, 1 2 1, 1, 1 1 1 2,
    #              2 2 1 1, 1 1 1 1 1, 1 2 2, 2 2, 1 1 1 1 1, 1 1 1 1, 1 1""")
    # ))
    # b.solve(print)

    # b = Board((
    #     parse("""2 4, 1 1 3 1, 6, 3 3, 3 4, 1 3 2, 3 4 1, 3 5 1 1, 12,
    #              5 3 3, 6 4, 2 3, 1 2 2, 3 4, 3 5"""),
    #     parse("""1 6, 2 2 4 2, 3 5 2, 11, 1 6 1, 4 1 5, 5 3 3, 10 2, 1 7 1 1, 5 1 1 1,
    #              1 3 1, 3, 3, 1 1, 3"""),
    # ))
    # b.solve()

    c = Board((
        parse("""1 5 2, 1 1 2, 1 1 2 1 2, 2 2, 2 1 1 1, 1 1 1, 1 1, 1 1 1, 2 3 1 1,
                 1 2 3 1 1, 1 3 1 1, 2 1 1 1, 1 1 1 2 1, 1 1 1 2 1, 2 1"""),
        parse("""1 2 1 1, 1 1 4, 2 1, 1 1 1 1 2, 1 3 1 1, 1 2, 1 1 1 1 1 1,
                 1 1 1 1 1 2, 1 1 2, 1 2 1 1, 3 1 4, 1 4 1, 3, 3 1 1, 1 2 1""")
    ))
    c.solve(print)

    # c = Board(([[2, 1], [2, 1, 1], [1, 1, 1, 1], [2, 1], [1, 1, 1], [1, 1, 1, 1], [3], [3, 2, 1], [1, 1, 3, 1],
    #  [1, 1, 1, 1], [1, 2, 1, 1, 1], [1, 1, 1, 1], [1, 2, 1], [1], [1, 4, 1]],
    #  [[1, 2, 1], [1, 3, 1], [1, 1, 3], [1, 1, 1], [1, 1], [1, 1], [1, 2, 1, 1, 1], [2, 3, 3, 1, 1],
    #  [1, 1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1], [1, 2], [1, 1], [1, 1, 1]]))
    # c.solve(print)

    if len(sys.argv) > 2:
        b = Board((parse(sys.argv[1]), parse(sys.argv[2])))
        b.solve(print)
