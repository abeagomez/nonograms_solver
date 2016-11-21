from itertools import combinations_with_replacement


def gen_lines(width, pattern):
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


def cdfs():
    pass
