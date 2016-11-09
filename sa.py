# Simulated annealing solution on a single game

from game import Game
from solution import LocalSearchSolution
import random as rd

MAX_ITERATIONS = 100001
T0 = 50
Tmin = 0.01
ALPHA = 0.95


def sa_solve(game: Game, error_list: list = [], tlist: list = [], plist: list = []):
    solution = LocalSearchSolution(game, next='iterative')
    it = 1
    error = solution.eval()
    temp = game.columns * game.rows / 4
    EQUILIBRIUM_COUNT = 10 * game.columns

    while it < MAX_ITERATIONS and error > 0:
        solution.next()
        new_error = solution.eval()
        p = np.exp((error - new_error) / temp)
        if new_error < error or p > rd.random():
            if new_error > error:
                tlist.append(temp)
                plist.append(p)
            error_list.append(error)
            error = new_error
        else:
            solution.go_back()
        if it % EQUILIBRIUM_COUNT == 0:
            temp *= ALPHA
            # if temp < Tmin:
            #     temp = Tmin
        it += 1

    return solution.board if error == 0 else None


if __name__ == '__main__':
    from generator import generate_board
    from matplotlib.pylab import *

    board = generate_board(10, 10)
    g = Game(board)
    g.print()
    print(board)
    print('\n------------------------\n')
    e = []
    t = []
    p = []
    print(sa_solve(g, e, t, p))
    plot(e, color='red')
    show()
    plot(t, color='blue')
    plot(p, color='green')
    show()
