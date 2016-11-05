from dfs import dfs_solve
from sa import sa_solve

if __name__ == '__main__':
    import time
    from generator import generate_board, generate_game
    from game import Game
    import random as rd

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
