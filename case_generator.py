from generator import generate_board
from game import Game


def generate_boards(n, size=10):
    l = []
    for i in range(n):
        b = generate_board(size, size)
        p = Game(b)
        l.append((size, [p.lists[1], p.lists[0]], b))
    return l


if __name__ == '__main__':
    a = generate_boards(1, 30)
    print(a[0][0], a[0][1])
