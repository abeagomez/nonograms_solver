# Local search with multiple restarts implementation for solving a single Picross Problem.
from game import Game
from solution import LocalSearchSolution

MAX_ITERATIONS = 100000


def ls(width: int, col_rest: list, row_rest: list):
    game = Game(None, width, width, lists=[row_rest, col_rest])
    return ls_solve(game)


def ls_solve(game: Game):
    it = 0
    solution = LocalSearchSolution(game, next='iterative')
    error = solution.eval()
    while it < MAX_ITERATIONS and error > 0:
        solution.next()
        e = solution.eval()
        if e > error:
            solution.go_back()
        else:
            error = e
        it += 1

    return solution.board if error == 0 else None


def lsmr(width: int, col_rest: list, row_rest: list):
    game = Game(None, width, width, lists=[row_rest, col_rest])
    return lsmr_solve(game)


def lsmr_solve(game: Game):
    it = 0
    solution = LocalSearchSolution(game, next='iterative')
    error = solution.eval()
    ctr = 0
    while it < MAX_ITERATIONS and error > 0:
        solution.next()
        e = solution.eval()
        if e > error:
            solution.go_back()
            ctr += 1
        else:
            ctr = 0
            error = e
        if ctr == 1000:
            print('Restart', error)
            solution = LocalSearchSolution(game, next='iterative')
            error = solution.eval()
        it += 1

    return solution.board if error == 0 else None


if __name__ == '__main__':
    from generator import generate_board

    b = generate_board(15, 15)
    g = Game(b)
    g.print()
    print(b)
    print('\n-----------------------\n')
    print(lsmr_solve(g))
