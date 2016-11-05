from game import *


def dfs_solve(game: Game):
    return dfs(game, Bitset(game.rows, game.colums))

def dfs(game: Game, board: Bitset, pos: int = 0):
    if pos == Game.rows*Game.colums:
        # Check
        pass


if __name__ == '__main__':
    import time

    a = time.time()
    for i in range(1 << 27):
        pass
    b = time.time()
    print(b - a)
