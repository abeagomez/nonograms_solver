from generator import *
import json
import numpy as np


class Game:
    def __init__(self, board: Bitset, n: int, m: int, lists: list = None):
        if lists:
            self.lists = lists
        elif board:
            self.lists = generate_game(board)
            n, m = board.rows, board.columns
        else:
            board = generate_board(n, m)
            self.lists = generate_game(b)

        self.rows = n
        self.colums = m

    def save(self, filename: str):
        with open(filename, 'w')  as file:
            json.dump(
                {'l': self.lists, 'rows': self.rows, 'columns': self.colums},
                file)

    @staticmethod
    def load(filename: str):
        with open(filename) as file:
            l = json.load(file)
            return Game(None, n=l['rows'], m=l['columns'], lists=l['l'])

    def print(self):
        k = '\t' + '\t'.join(map(lambda x: str(x), self.lists[1]))
        print(k)
        for i in self.lists[0]:
            print(i)

    def check(self, board: Bitset):
        l = np.array(generate_game(board))
        k = np.array(self.lists)
        if board.rows == board.columns:
            return all([all(g) for g in (l  == k)])
        else:
            return all(l==k)

if __name__ == '__main__':
    b = generate_board(50, 4)
    g = Game(b, 50, 4)
    g.save('pepe.game')
    g = Game.load('pepe.game')
    print(g.check(b))
