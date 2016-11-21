from generator import generate_board
from game import Game
import random as rd


def generate_boards(n, size=10, prob=None):
    l = []
    for i in range(n):
        uprob = rd.random() if prob is None else prob
        b = generate_board(size, size, uprob)
        p = Game(b)
        l.append((size, [p.lists[1], p.lists[0]], b))
    return l


if __name__ == '__main__':
    a = generate_boards(1, 3)
    print(a[0][0], a[0][1])
