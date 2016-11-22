import numpy as np
import heapq as heap


class PriorityQueue:
    def __init__(self, maxim=False):
        self.heap = []
        self.count = 0
        self.reverse = dict()
        self.maxim = maxim

    def push(self, value, item):
        if self.maxim:
            value = - value

        if self.reverse.get(item):
            self.heap.remove((self.reverse[item], item))

        self.reverse[item] = value
        self.heap.append((value, item))
        heap.heapify(self.heap)
        self.count += 1

    def pop(self):
        _, item = heap.heappop(self.heap)
        self.reverse[item] = None
        self.count -= 1
        return item

    def isEmpty(self):
        return self.count == 0

    def __str__(self):
        return str(self.heap)


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


class Problem:
    def __init__(self, column_restrictions, row_restrictions, another_problem=None):
        self.columns = column_restrictions
        self.rows = row_restrictions
        # Assuming square problems
        self.width = len(column_restrictions)
        self.board = -np.ones((self.width, self.width), np.int) \
            if another_problem is None else another_problem.board.copy()
        self.densities = PriorityQueue(True) \
            if another_problem is None else another_problem.densities
        if another_problem is None:
            self.calculate_densities()
        self.ok = True

    def copy(self):
        return Problem(self.columns, self.rows, self)

    def fix_line(self, line):
        i = line[0]
        constrains = (self.row(i) if line[1] == 'R' else self.column(i)).copy()

        pattern = self.rows[i] if line[1] == 'R' else self.columns[i]
        all_solutions = [np.array([0] * self.width)] if len(pattern) == 0 else \
            [np.array(expand_solution(x, self.width, pattern))
             for x in solutions(self.width, pattern, constrains)]

        if len(all_solutions) == 0:
            print('WTF')
            self.ok = False
            return []

        ac = all_solutions[0]
        equals = None
        for sol in all_solutions[1:]:
            equals = (ac == sol)
            ac = -np.ones(self.width, np.int)
            ac[equals] = sol[equals]

        if line[1] == 'R':
            self.set_row(i, ac)
        else:
            self.set_column(i, ac)

        upd = np.array([x for x in range(self.width)])[ac != constrains]
        return [(x, y) for x, y in zip(upd, len(upd) * ['C' if line[1] == 'R' else 'R'])]

    def initial_fix(self):
        s = set()
        while not self.densities.isEmpty() or len(s) != 0:
            line = self.densities.pop() if len(s) == 0 else s.pop()
            l2 = self.fix_line(line)
            for i in l2:
                s.add(i)

    def fix_pos(self, r, c):
        s = set([(r, 'R'), (c, 'C')])
        while len(s) != 0:
            line = s.pop()
            self.fix_line(line)
            if not self.ok:
                return False
        return True

    def calculate_densities(self):
        for i in range(self.width):
            self.densities.push(sum(self.columns[i]) / self.width, (i, 'C'))
            self.densities.push(sum(self.rows[i]) / self.width, (i, 'R'))

    def set_value(self, r, c, value):
        self.board[r, c] = value

    def row(self, i):
        return self.board[i]

    def column(self, i):
        return self.board.T[i]

    def set_row(self, i, value):
        """
        :param i: Index of the row
        :param value: Must be a ndarray of shape (self.width,)
        :return: None
        """
        self.board[i] = value

    def set_column(self, i, value):
        """
        :param i: Index of the row
        :param value: Must be a ndarray of shape (self.width,)
        :return: None
        """
        self.board.T[i] = value


if __name__ == '__main__':
    from case_generator import generate_boards
    from pprint import pprint

    a = generate_boards(1, 5, 0.4)
    a = a[0]
    print(a[2])
    print(a[1])
    p = Problem(a[1][0], a[1][1])

    # El caso que rompe el código de generar soluciones de Andy
    # p = Problem([[1], [1], [3], [3], [1, 1], [1, 4]], [[1], [2], [4], [2, 1], [2], [2, 1]])

    # Uff que es esto????
    # Fiu era que había copiado mal el caso siempre daba que no tenía solución.
    #
    # XX...
    # XXX..
    # X...X
    # .XXX.
    # ...XX
    #
    # p = Problem([[2], [2, 1], [1, 1], [2], [1, 1]], [[2], [3], [1, 1], [3], [2]])

    # Este caso no adivina nada
    #
    # .....X....
    # X..X.X...X
    # .X....X..X
    # .XX.X...XX
    # .X.X.X....
    # X...X....X
    # X.X.X...X.
    # .X........
    # ....X.X.X.
    # ....X.XX..
    #

    #
    # .XX..
    # .XX.X
    # X...X
    # ..X..
    # X...X
    #
    # p = Problem([[1, 1], [2], [2, 1], [], [2, 1]], [[2], [2, 1], [1, 1], [1], [1, 1]])

    p.initial_fix()
    pprint(p.board)
    print(p.ok)
