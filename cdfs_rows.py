from itertools import combinations_with_replacement
from cdfs_box import Stack, problem, build_board
from pprint import pprint


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


def expand_solution(solution, width, pattern):
    """
    expands a solution to a tuple of 1 (ON) and 0 (OFF)
    """
    r = []
    for s, p in zip(solution, pattern):
        r.extend([False] * s)
        r.extend([True] * p)
    r.extend([False] * (width - sum(solution) - sum(pattern)))
    return r


def cdfs(width: int, col_rest: list, row_rest: list):
    board = build_board(width)
    p = problem(col_rest, row_rest, width, board)
    stack = Stack()

    # Each state is the current status of the problem and the index of the row being analyzed.
    stack.push((p, 0))

    while not stack.isEmpty():
        p, row = stack.pop()
        assert isinstance(p, problem)
        if row >= width:
            # Found (only reaches this point if all rows were correct)
            return p.board

        np = problem(col_rest, row_rest, width, p.copy_board())

        for sol in gen_lines(width, row_rest[row]):
            sol = expand_solution(sol, width, row_rest[row])
            np.board[row] = sol
            res = True
            for i in range(width):
                idx = row * width + i

                if sol[i] is True:
                    b = np.check_column_when_set_true(np.current_column(i), idx)
                else:
                    b = np.check_column_when_set_false(np.current_column(i), idx)

                res &= b
                if not res:
                    break
            if res:
                nnp = problem(col_rest, row_rest, width, np.copy_board())
                stack.push((nnp, row + 1))

    return None


if __name__ == '__main__':
    from case_generator import generate_boards

    for a in generate_boards(1, 15, 0.3):
        pprint(cdfs(a[0], a[1][0], a[1][1]))

# print(a[2])
#     print("""XX.X
# XXX.
# XXX.
# X.X.""")
#     print('---------------')
#     print('[[[4], [3], [3], [1]], [[2, 1], [3], [3], [1, 1]]]')
#     print('---------------')
#     pprint(cdfs(a[0], [[4], [3], [3], [1]], [[2, 1], [3], [3], [1, 1]]))
