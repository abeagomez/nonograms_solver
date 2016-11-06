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


def ls_generate_initial(game: Game):
    columns = game.columns

    solution = []

    # Go through the horizontals
    for line in game.lists[0]:
        s = sum(line)
        rem = columns - s
        l = np.ones(len(line) + 1, int)
        rem -= (len(line) - 1)
        l[0] = 0
        l[-1] = 0
        while rem > 0:
            idx = rd.randint(0, len(l) - 1)
            l[idx] += 1
            rem -= 1
        solution.append(l.tolist())

    return solution


def ls_generate_next(board: Bitset):
    pass


def ls_eval(game: Game, board: Bitset):
    pass


def ls_solve(game: Game):
    pass


if __name__ == '__main__':
    from generator import generate_board

    board = generate_board(5, 5)
    # board = Bitset(2, 2)
    # board[0, 1] = True
    # board[1, 0] = True
    game = Game(board)
    sol = ls_generate_initial(game)
    board2 = board_from_solution(game, sol)
    game.print()
    # board2 = Bitset(2, 2)
    # board2[0, 1] = True
    # board2[1, 1] = True
    print(board, board2, sep='\n\n')
    print(game.check_horizontal(board2))
    print(game.check_vertical(board2))
