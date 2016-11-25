# DFS full search solution to a single game
# only works (in a reasonable time) for games of at most 20 cells

from game import *


def dfs(width: int, col_rest: list, row_rest: list):
    game = Game(None, width, width, lists=[row_rest, col_rest])
    return dfs_solve(game)


def dfs_solve(game: Game):
    return dfs_internal(game, Bitset(game.rows, game.columns))


def dfs_internal(game: Game, board: Bitset, pos: int = 0):
    if pos == game.rows * game.columns:
        if game.check(board):
            return board
        return None
    row = pos // board.columns
    column = pos % board.columns
    board[row, column] = True
    r = dfs_internal(game, board, pos + 1)
    if r: return r
    board[row, column] = False
    r = dfs_internal(game, board, pos + 1)
    if r: return r
    return None


if __name__ == '__main__':
    print(dfs(3, [[1], [], []], [[], [], [1]]))
