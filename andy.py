#!/usr/bin/env python3

from itertools import combinations_with_replacement


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


if __name__ == "__main__":

    for i in solve1(10, [8]):
        print(i)
