# DFS full search solution to a single game
# only works (in a reasonable time) for games of at most 20 cells

from game import *


def dfs_solve(game: Game):
    return dfs(game, Bitset(game.rows, game.columns))


def dfs(game: Game, board: Bitset, pos: int = 0):
    if pos == game.rows * game.columns:
        if game.check(board):
            return board
        return None
    row = pos // board.columns
    column = pos % board.columns
    board[row, column] = True
    r = dfs(game, board, pos + 1)
    if r: return r
    board[row, column] = False
    r = dfs(game, board, pos + 1)
    if r: return r
    return None
