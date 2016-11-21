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


def build_board(size):
    board = []
    for i in range(0, size):
        l = []
        for j in range(0, size):
            l.append(False)
        board.append(l)
    return board


class problem:
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
        # Check if previous line is OK
        if not self.check_previous_row(index): return False
        row = self.current_row(index)
        column = self.current_column(index)
        column_index = self.current_column_index(index)
        if row[column_index]:
            if self.checkline(row, self.restrictions_rows[self.current_row_index(index)],
                              self.current_column_index(index)) and self.checkline(column, self.restrictions_columns[
                self.current_column_index(index)], self.current_row_index(index)):
                return True
        else:
            if self.check_inFalse_line(row, self.restrictions_rows[self.current_row_index(index)],
                                       self.current_column_index(index)) and self.check_inFalse_line(column,
                                                                                                     self.restrictions_columns[
                                                                                                         self.current_column_index(
                                                                                                             index)],
                                                                                                     self.current_row_index(
                                                                                                         index)):
                return True
        return False

    def check_previous_row(self, index):
        previous_row_index = self.current_row_index(index) - 1
        if self.current_column_index(index) is 0 and previous_row_index >= 0:
            row = self.current_row(index - 1)
            if self.check_whole_line(row, self.restrictions_rows[previous_row_index]):
                return True
            return False
        return True

    def check_rest_of_line(self, line, restrictions, line_blocks, index, mark):
        if mark:
            # restriction number n
            n_res = restrictions[len(line_blocks) - 1]
            if n_res < line_blocks[-1]: return False
            rest = n_res - line_blocks[-1]
            s = 0
            for i in range(len(line_blocks), len(restrictions)):
                s += restrictions[i] + 1
            rest = rest + s
            if len(line) - (index + 1) < rest: return False
            return True
        else:
            s = 0
            if line_blocks[-1] is not 0:
                for i in range(len(line_blocks), len(restrictions)):
                    s += restrictions[i] + 1
            else:
                for i in range(0, len(restrictions)):
                    s += restrictions[i] + 1

            s -= 1
            if len(line) - (index + 1) < s: return False
            return True

    def check_inFalse_line(self, line, restrictions, index):
        result = self.simple_split(line)
        line_blocks = result[0]
        # index = result[1]
        for i in range(0, len(line_blocks) - 1):
            if restrictions[i] != line_blocks[i]: return False
        if not self.check_rest_of_line(line, restrictions, line_blocks, index, False): return False
        return True

    def checkline(self, line, restrictions, index):
        result = self.simple_split(line)
        line_blocks = result[0]
        # index = result[1]
        # If I have more blocks than restrictions, return False
        if len(restrictions) < len(line_blocks): return False
        # If I have a wrong-size block so far, return False
        # Unnecesary condition so far...len(line_blocks) is always at least 1
        # if len(line_blocks) > 0:
        for i in range(0, len(line_blocks) - 1):
            if restrictions[i] != line_blocks[i]: return False
        if not self.check_rest_of_line(line, restrictions, line_blocks, index, True): return False
        return True

    def check_board(self):
        for i in range(0, self.size):
            column = self.current_column(i)
            if not self.check_whole_line(column, self.restrictions_columns[i]): return False
            row = self.current_row(i * self.size)
            if not self.check_whole_line(row, self.restrictions_rows[i]): return False
        return True

    def simple_split(self, line):
        split_blocks = []
        current = 0
        n = 0
        index = 0
        while n < len(line):
            while n < len(line) and not line[n]:
                n += 1
            while n < len(line) and line[n]:
                current += 1
                n += 1
            if current > 0:
                index = n
                split_blocks.append(current)
            current = 0
        if len(split_blocks) is 0:
            split_blocks.append(0)
        return (split_blocks, index)

    def check_whole_line(self, line, restrictions):
        line_blocks = self.simple_split(line)[0]
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


def cdfs(size, restrictions_columns, restrictions_rows):
    board = build_board(size)
    p = problem(restrictions_columns, restrictions_rows, size, board)
    s = Stack()
    s.push((p, 0))
    while not s.isEmpty():
        current_element = s.pop()
        current_problem = current_element[0]
        current_index = current_element[1]
        if current_problem.check_board():
            current_problem.board
            return current_problem.board
        if current_index > size * size:
            continue
        p_right = problem(current_problem.restrictions_columns,
                          current_problem.restrictions_rows,
                          current_problem.size,
                          current_problem.copy_board())
        p_right.set_value(current_index, False)
        p_left = problem(current_problem.restrictions_columns,
                         current_problem.restrictions_rows,
                         current_problem.size,
                         current_problem.copy_board())
        p_left.set_value(current_index, True)
        new_index = current_index + 1

        if p_right.check_current_line(current_index):
            s.push((p_right, new_index))
        if p_left.check_current_line(current_index):
            s.push((p_left, new_index))
    return []


print(cdfs(3, [[2], [0], [1]], [[1, 1], [1], [0]]))
