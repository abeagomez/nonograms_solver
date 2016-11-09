def build_board(size):
    board = []
    for i in range(0, size):
        l = []
        for j in range(0, size):
            l.append(False)
        board.append(l)
    return board


class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."

    def __init__(self):
        self.list = []

    def push(self, item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0


class Problem:
    def __init__(self, restrictions_columns, restrictions_rows, size, board):
        self.restrictions_columns = restrictions_columns
        self.restrictions_rows = restrictions_rows
        self.size = size
        self.board = board

    def current_row_index(self, index):
        return index // self.size

    def current_column_index(self, index):
        return index % self.size

    def set_value(self, index, value):
        self.board[self.current_row_index(index)][self.current_column_index(index)] = value

    def current_row(self, index):
        index = self.current_row_index(index)
        row = []
        for i in range(0, self.size):
            row.append(self.board[index][i])
        return row

    def current_column(self, index):
        index = self.current_column_index(index)
        column = []
        for i in range(0, self.size):
            column.append(self.board[i][index])
        return column

    def check_current_line(self, index):
        row = self.current_row(index)
        column = self.current_column(index)
        return self.checkline(row, self.restrictions_rows[self.current_row_index(index)]) \
               and self.checkline(column, self.restrictions_columns[self.current_column_index(index)])

        # return True
        # return False

    def checkline(self, line, restrictions):
        line_blocks = self.simple_split(line)
        # If I have more blocks than restrictions, return False
        if len(restrictions) < len(line_blocks): return False
        # If I have a wrong-size block so far, return False
        if len(line_blocks) > 0:
            for i in range(0, len(line_blocks) - 1):
                if restrictions[i] != line_blocks[i]: return False
            if restrictions[len(line_blocks) - 1] < line_blocks[len(line_blocks) - 1]: return False
        return True

    def check_board(self):
        for i in range(0, self.size):
            column = self.current_column(i)
            if not self.check_whole_line(column, self.restrictions_columns[i]): return False
            row = self.current_row(i * self.size)
            if not self.check_whole_line(row, self.restrictions_rows[i]): return False
        return True

    def dummy_check(self, line_blocks, line, restrictions):
        if restrictions[len(line_blocks) - 1] < line_blocks[len(line_blocks) - 1]: return False
        return True

    def simple_check(self, line_blocks, line, restrictions):
        pass

    # last_block_size = line_blocks[len(line_blocks)-1]
    # last_restriction_matters = restrictions[len(line_blocks)-1]
    # if last_restriction_matters < last_block_size and : return False

    def simple_split(self, line):
        split_blocks = []
        current = 0
        n = 0
        while n < len(line):
            while n < len(line) and not line[n]:
                n += 1
            while n < len(line) and line[n]:
                current += 1
                n += 1
            if current > 0:
                split_blocks.append(current)
            current = 0
        if len(split_blocks) is 0:
            split_blocks.append(0)
        return split_blocks

    def check_whole_line(self, line, restrictions):
        line_blocks = self.simple_split(line)
        if len(line_blocks) != len(restrictions): return False
        for i in range(0, len(restrictions)):
            if line_blocks[i] != restrictions[i]:
                return False
        return True

    def copy_board(self):
        board = []
        for i in self.board:
            l = []
            for j in range(0, len(i)):
                l.append(i[j])
            board.append(l)
        return board


def cdfs_solve(size, restrictions_columns, restrictions_rows):
    board = build_board(size)
    p = Problem(restrictions_columns, restrictions_rows, size, board)
    s = Stack()
    s.push((p, 0))
    while not s.isEmpty():
        current_element = s.pop()
        current_problem = current_element[0]
        current_index = current_element[1]
        if current_problem.check_board():
            print(current_problem.board)
            return current_problem.board
        p_right = Problem(current_problem.restrictions_columns,
                          current_problem.restrictions_rows,
                          current_problem.size,
                          current_problem.copy_board())
        p_right.set_value(current_index, False)
        p_left = Problem(current_problem.restrictions_columns,
                         current_problem.restrictions_rows,
                         current_problem.size,
                         current_problem.copy_board())
        p_left.set_value(current_index, True)
        new_index = current_index + 1
        if new_index < size * size:
            """
            print "current right board"
            print p_right.board
            print p_right.check_current_line(current_index)
            print ""
            print "current left board"
            print p_left.board
            print p_left.check_current_line(current_index)
            print current_index
            print ""
            """

            if p_right.check_current_line(current_index):
                s.push((p_right, new_index))
            if p_left.check_current_line(current_index):
                s.push((p_left, new_index))
    print("Not found")
    return []


cdfs_solve(3, [[2],
               [0],
               [1]],
           [[1, 1],
            [1],
            [0]])

# cdfs_solve(10, [[3, 5],
#          [4, 1, 1],
#          [2, 2, 1],
#          [1, 2, 2],
#          [1, 1, 1, 1],
#          [1, 2, 1, 1],
#          [1, 1, 2],
#          [2, 2, 1],
#          [4, 1, 1],
#          [3, 5]],
#     [[4],
#      [3, 3],
#      [3, 1, 3],
#      [2, 3, 2],
#      [1, 1, 1, 1],
#      [1, 1],
#      [1, 1, 2, 1, 1],
#      [3, 3],
#      [1, 1, 1, 1],
#      [10]])


# board = build_board(3)
# p = problem([[1,1],[1],[0]], [[2],[0],[1]], 3, board)
# print p.board
# p2 = problem(p.restrictions_columns, p.restrictions_rows, p.size, p.copy_board())
# p3 = problem(p.restrictions_columns, p.restrictions_rows, p.size, p.copy_board())
# print p2.board
# print p3.board

# p2.set_value(1, True)
# print ""
# print p2.board
# print ""
# print p3.

# p = problem([[2],[0],[1]],[[1,1],[1],[0]], 3, [[True, False, True], [True, False, False], [False, False, False]])
# print p.check_board()
