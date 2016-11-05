from generator import *
import json
import numpy as np


class Game:
    """
    Representation of a Picross Game
    """

    def __init__(self, board: Bitset, n: int = None, m: int = None, lists: list = None):
        if lists:
            self.lists = lists
        elif board:
            self.lists = generate_game(board)
            n, m = board.rows, board.columns
        else:
            board = generate_board(n, m)
            self.lists = generate_game(b)

        self.rows = n
        self.columns = m

    def save(self, filename: str):
        with open(filename, 'w')  as file:
            json.dump(
                {'l': self.lists, 'rows': self.rows, 'columns': self.columns},
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
        b = (l == k)
        if isinstance(b, np.bool_) or isinstance(b, bool):
            return b
        return all((l == k).flatten())

    def eval(self, board: Bitset):
        pass


if __name__ == '__main__':
    b = generate_board(50, 4)
    g = Game(b, 50, 4)
    g.save('pepe.game')
    g = Game.load('pepe.game')
    print(g.check(b))
