# Local search with multiple restarts implementation for solving a single Picross Problem.
from bitset import Bitset
from game import Game
import numpy as np
import random as rd


def board_from_solution(game: Game, solution: list):
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
    return board


def ls_generate_row(line: np.ndarray, count: int):
    s = sum(line)
    rem = count - s
    l = np.ones(len(line) + 1, int)
    rem -= (len(line) - 1)
    l[0] = 0
    l[-1] = 0
    while rem > 0:
        idx = rd.randint(0, len(l) - 1)
        l[idx] += 1
        rem -= 1
    return l


def ls_generate_initial(game: Game):
    columns = game.columns

    solution = []

    # Go through the horizontals
    for line in game.lists[0]:
        solution.append(ls_generate_row(line, columns))

    return solution


def ls_generate_random_next(game: Game, solution: list):
    i = rd.randint(0, len(solution) - 1)
    gen = 1
    ct = 0
    while np.all(np.array(game.lists[0][i]) <= 1):
        i = rd.randint(0, len(solution) - 1)
        if ct == game.max_random_generations: return False
        ct += 1

    while True:
        l = ls_generate_row(game.lists[0][i], game.columns)
        b = l == solution[i]
        if not np.all(b):
            solution[i] = l
            return True
        if ct == game.max_random_generations: return False
        i = rd.randint(0, len(solution) - 1)
        ct += 1


def ls_generate_iterative_next(game: Game, solution: list):
    i = game.last_changed_row
    initial_i = i
    while np.all(np.array(game.lists[0][i]) <= 1):
        game.increase_last_change()
        i = game.last_changed_row
        if i == initial_i: return False

    while True:
        l = ls_generate_row(game.lists[0][i], game.columns)
        b = l == solution[i]
        if not np.all(b):
            solution[i] = l
            return True
        game.increase_last_change()
        i = game.last_changed_row
        if i == initial_i: return False


def ls_generate_next(game: Game, solution: list):
    ls_generate_random_next(game, solution)
    # ls_generate_iterative_next(game, solution)


def ls_eval(game: Game, board: Bitset):
    pass


def ls_solve(game: Game):
    raise NotImplementedError()


if __name__ == '__main__':
    from generator import generate_board

    board = generate_board(5, 5)
    game = Game(board)
    sol = ls_generate_initial(game)
    board2 = board_from_solution(game, sol)
    game.print()
    print(board, board2, sep='\n\n')
    print(game.check_horizontal(board2))
    print(game.check_vertical(board2), '\n')

    ls_generate_next(game, sol)
    print(board_from_solution(game, sol), '\n')
    ls_generate_next(game, sol)
    print(board_from_solution(game, sol), '\n')
    ls_generate_next(game, sol)
    print(board_from_solution(game, sol), '\n')
