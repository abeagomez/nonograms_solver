from generator import *
import json
import numpy as np


class Game:
    def __init__(self, board: Bitset = None, n: int = None, m: int = None):
        if board:
            self.lists = generate_game(board)
        elif n is not None and m is not None:
            b = generate_board(n, m)
            self.lists = generate_game(b)

    @staticmethod
    def __from_lists(lists: list):
        g = Game()
        g.lists = lists
        return g

    def save(self, filename: str):
        with open(filename, 'w')  as file:
            json.dump(self.lists, file)

    @staticmethod
    def load(filename: str):
        with open(filename) as file:
            l = json.load(file)
            return Game.__from_lists(l)

    def print(self):
        k = '\t' + '\t'.join(map(lambda x: str(x), self.lists[1]))
        print(k)
        for i in self.lists[0]:
            print(i)

    def check(self, board: Bitset):
        l = np.array(generate_game(board))
        k = np.array(self.lists)
        return all([all(g) for g in (l == k)])


if __name__ == '__main__':
    b = generate_board(5, 5)
    g = Game(b)
    g.save('pepe.game')
    g = Game.load('pepe.game')
    print(g.check(b))
