import random as rd
from bitset import Bitset


def generate_board(n: int, m: int):
    """
    Generates a random matrix of NxM cells where every cell has a 50% probablility of being marked or not.
    """
    b = Bitset(n, m)
    for i in range(n):
        for j in range(m):
            if rd.random() > 0.5:
                b[i, j] = True
    return b


def generate_game(board: Bitset):
    """
    Given a fixed board, generates the Picross Game representation.
    """
    hor = []
    ver = []
    for i in range(board.rows):
        current = 0
        same = False
        l = []
        for j in range(board.columns):
            if board[i, j]:
                current += 1
                same = True
            elif same:
                l.append(current)
                current = 0
                same = False
        if current > 0:
            l.append(current)

        hor.append(l)

    for j in range(board.columns):
        current = 0
        same = False
        l = []
        for i in range(board.rows):
            if board[i, j]:
                current += 1
                same = True
            elif same:
                l.append(current)
                current = 0
                same = False
        if current > 0:
            l.append(current)
        ver.append(l)

    return hor, ver


if __name__ == "__main__":
    board = generate_board(5, 5)
    board.print()
    game = generate_game(board)
    print(game[0], "\n", game[1])
