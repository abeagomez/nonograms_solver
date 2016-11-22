import numpy as np


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
        e = expand_solution((gap,), gap + p + 1, (p,))
        if not matches(e, constraints[:gap + p + 1]):
            continue
        if len(pattern) == 1:
            yield (gap,)
            continue
        subwidth = width - gap - p - 1
        subpattern = pattern[1:]
        subconstraints = constraints[-subwidth:]
        for s in solve2(subwidth, subpattern, subconstraints):
            yield (gap, s[0] + 1) + s[1:]


def line_density(line):
    line = np.array(line)
    return len(line[line])


def get_restrictions(width, pattern):
    pass


class Problem:
    def __init__(self, columns_restrictions, rows_restrictions, board, fixed_positions):
        self.columns_restrictions = columns_restrictions
        self.rows_restrictions = rows_restrictions
        self.columns_density = [line_density(x) for x in self.columns_restrictions]
        self.rows_density = [line_density(x) for x in self.rows_restrictions]
        self.size = len(columns_restrictions), len(rows_restrictions)
        self.board = board
        self.fixed_positions = fixed_positions

    def valid_combinations(self, line):
        pass

    def sads(self):
        c_index = np.argmax(self.columns_density)
        r_index = np.argmax(self.rows_density)
        line = self.columns_restrictions[c_index] \
            if self.columns_density[c_index] > self.rows_density[r_index] \
            else self.rows_restrictions[r_index]

        combinations = self.valid_combinations(line)


if __name__ == '__main__':
    rest = [2, 3, 2]
    for i in solve2(10, rest, []):
        print(expand_solution(i, 10, rest))
