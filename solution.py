from game import Game
from bitset import Bitset
import numpy as np
import random as rd
from generator import generate_game


class LocalSearchSolution:
    def __init__(self, game: Game, initial: str = 'random', next: str = 'random'):
        self.game = game
        self.lists = []
        self.generate_initial(initial)
        self.board_updated = False
        self._board = None
        self.max_random_generations = 10
        self.old_state = None
        self.last_changed_row = 0
        self.next_type = next

    @property
    def board(self):
        if self._board and self.board_updated:
            return self._board
        return self.generate_board()

    def leftmost(self):
        solution = []
        # Go through the horizontals
        for line in self.game.lists[0]:
            s = sum(line)
            rem = self.game.columns - s
            l = np.ones(len(line) + 1, int)
            rem -= (len(line) - 1)
            l[0] = 0
            l[-1] = 0
            l[-1] += rem
            solution.append(l)

        self.lists = solution

    def rightmost(self):
        solution = []
        # Go through the horizontals
        for line in self.game.lists[0]:
            s = sum(line)
            rem = self.game.columns - s
            l = np.ones(len(line) + 1, int)
            rem -= (len(line) - 1)
            l[0] = 0
            l[-1] = 0
            l[0] += rem
            solution.append(l)

        self.lists = solution

    def generate_board(self):
        game = self.game
        solution = self.lists
        board = Bitset(game.rows, game.columns)
        for i, line in enumerate(solution):
            game_line = game.lists[0][i]
            sol_line = solution[i]
            idx = 0
            for k in range(len(sol_line) - 1):
                idx += sol_line[k]
                for j in range(game_line[k]):
                    board[i, idx] = True
                    idx += 1
        self._board = board
        self.board_updated = True
        return board

    def generate_row(self, line: np.ndarray):
        s = sum(line)
        rem = self.game.columns - s
        l = np.ones(len(line) + 1, int)
        rem -= (len(line) - 1)
        l[0] = 0
        l[-1] = 0
        while rem > 0:
            idx = rd.randint(0, len(l) - 1)
            l[idx] += 1
            rem -= 1
        return l

    def generate_initial(self, kind: str):
        if kind == 'leftmost':
            self.leftmost()
        elif kind == 'rightmost':
            self.rightmost()
        else:
            game = self.game
            solution = []
            # Go through the horizontals
            for line in game.lists[0]:
                solution.append(self.generate_row(line))
            self.lists = solution

    def generate_random_next(self):
        self.board_updated = False
        i = rd.randint(0, len(self.lists) - 1)
        solution = self.lists
        game = self.game
        ct = 0
        while np.all(np.array(game.lists[0][i]) <= 1):
            i = rd.randint(0, len(solution) - 1)
            if ct == self.max_random_generations: return False
            ct += 1

        while True:
            l = self.generate_row(game.lists[0][i])
            b = l == solution[i]
            if not np.all(b):
                self.old_state = i, solution[i]
                solution[i] = l
                return True
            if ct == self.max_random_generations: return False
            i = rd.randint(0, len(solution) - 1)
            ct += 1

    def generate_iterative_next(self):
        self.board_updated = False
        game = self.game
        solution = self.lists
        i = self.last_changed_row
        initial_i = i
        while np.all(np.array(game.lists[0][i]) <= 1):
            self.last_changed_row = (self.last_changed_row + 1) % self.game.columns
            i = self.last_changed_row
            if i == initial_i: return False

        while True:
            l = self.generate_row(game.lists[0][i])
            b = l == solution[i]
            if not np.all(b):
                self.old_state = i, solution[i]
                solution[i] = l
                self.last_changed_row = (self.last_changed_row + 1) % self.game.columns
                return True
            self.last_changed_row = (self.last_changed_row + 1) % self.game.columns
            i = self.last_changed_row
            if i == initial_i: return False

    def next(self):
        if self.next_type == 'iterative':
            return self.generate_iterative_next()
        else:
            return self.generate_random_next()

    def go_back(self):
        if self.old_state:
            self.lists[self.old_state[0]] = self.old_state[1]
            self.old_state = None
            self.board_updated = False

    def eval(self):
        _, v = generate_game(self.board)
        k = self.game.lists[1]
        error = 0
        for i in range(len(v)):
            line = v[i]
            correct = k[i]
            error += abs(len(line) - len(correct))
            for j in range(min(len(line), len(correct))):
                if line[j] != correct[j]: error += 1
        return error


if __name__ == '__main__':
    from generator import generate_board

    board = generate_board(5, 5)
    game = Game(board)
    sol = LocalSearchSolution(game)
    lsol = LocalSearchSolution(game, initial='leftmost')
    rsol = LocalSearchSolution(game, initial='rightmost')
    print('leftmost', lsol.board, sep='\n')
    print('rightmost', rsol.board, sep='\n')
    board2 = sol.board
    game.print()
    print(board, board2, sep='\n\n')
    print(game.check_horizontal(board2))
    print(game.check_vertical(board2), '\n')

    sol.next()
    print(sol.board, '\n')
    sol.next()
    print(sol.board, '\n')
    sol.next()
    print(sol.board, '\n')
    sol.go_back()
    print(sol.board, '\n')
    sol.next()
    print(sol.board, '\n')
    sol.next()
    print(sol.board, '\n')

    print(sol.eval())
