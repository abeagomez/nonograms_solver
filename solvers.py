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


if __name__ == '__main__':
    import time

    while True:
        # a = time.time()
        try:
            r = rd.randint(1, 8)
            c = rd.randint(1, 20 // r)
        except ValueError:
            continue

        print('--------------------------------\n')
        print(r, c)
        board = generate_board(r, c)
        game = Game(board)
        answer = dfs_solve(game)
        if answer != board:
            print("Different Answers:")
            game.print()
            print()
            print(board)
            print('\n')
            print(answer)
            print('--------------------------------\n')
        # b = time.time()
        # print(b - a)
        # print('--------------------------------\n\n')
        pass
