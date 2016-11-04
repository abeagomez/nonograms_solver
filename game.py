from generator import *
import json


class Game:
    def __init__(self, board: Bitset = None, n: int = None, m: int = None):
        if board:
            self.lists = generate_game(board)
        elif n is not None and m is not None:
            self.lists = generate_game(generate_board(n, m))

    @staticmethod
    def __from_lists(lists):
        g = Game()
        g.lists = lists
        return g

    def save(self, filename):
        with open(filename, 'w')  as file:
            json.dump(self.lists, file)

    @staticmethod
    def load(filename):
        with open(filename) as file:
            l = json.load(file)
            return Game.__from_lists(l)

    def print(self):
        k = '\t' + '\t'.join(map(lambda x: str(x), self.lists[1]))
        print(k)
        for i in self.lists[0]:
            print(i)

    def check(self, board:Bitset):
        pass

if __name__ == '__main__':
    g = Game(n=5, m=5)
    g.save('pepe.game')
    g = Game.load('pepe.game')
    g.print()
