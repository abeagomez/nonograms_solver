import unittest
from bitset import Bitset
from generator import generate_board
from game import Game
from solvers import dfs_solve
from ls import ls_generate_initial, board_from_solution, ls_generate_next


class BitsetTest(unittest.TestCase):
    def setUp(self):
        self.rows = 6
        self.columns = 5
        self.bitset = Bitset(self.rows, self.columns)

    def test_size(self):
        rows, columns = self.rows, self.columns
        a = self.bitset
        self.assertEqual(rows, a.rows)
        self.assertEqual(columns, a.columns)

    def test_indexing(self):
        a = self.bitset
        with self.assertRaises(IndexError):
            b = a[100, 100]
        with self.assertRaises(IndexError):
            a[100, 100] = False

    def test_ok(self):
        a = self.bitset
        a[2, 2] = True
        a[0, 1] = True
        self.assertTrue(a[2, 2])
        self.assertTrue(a[0, 1])
        self.assertFalse(a[0, 0])
        a[0, 1] = False
        self.assertFalse(a[0, 1])

    def test_equal(self):
        a = Bitset(3, 3)
        b = Bitset(3, 3)
        a[0, 0] = True
        self.assertNotEqual(a, b)
        b[0, 0] = True
        self.assertEqual(a, b)
        c = Bitset(4, 3)
        c[0, 0] = True
        self.assertNotEqual(a, c)

    def test_save_load(self):
        a = self.bitset
        a.save('test_board')
        b = Bitset.load('test_board')
        self.assertEqual(a, b)


class GameTest(unittest.TestCase):
    def setUp(self):
        self.rows = 3
        self.columns = 5
        self.board = generate_board(self.rows, self.columns)

    def test_generates_board(self):
        self.assertEqual(self.rows, self.board.rows)
        self.assertEqual(self.columns, self.board.columns)

    def test_generate_game(self):
        game = Game(self.board)
        self.assertEqual(game.rows, self.rows)
        self.assertEqual(game.columns, self.columns)
        self.assertTrue(game.check_horizontal(self.board))
        self.assertTrue(game.check_vertical(self.board))
        self.assertTrue(game.check(self.board))

    def test_save_load(self):
        game = Game(self.board)
        game.save('test_game')
        game = Game.load('test_game')


class DFSTest(unittest.TestCase):
    def setUp(self):
        self.board = generate_board(3, 3)
        self.game = Game(self.board)

    def test_dfs_solve(self):
        ans = dfs_solve(self.game)
        self.assertTrue(self.game.check(ans))


class MetaheuristicTest(unittest.TestCase):
    def setUp(self):
        self.board = generate_board(4, 10)
        self.game = Game(self.board)

    def test_initial_solution(self):
        sol = ls_generate_initial(self.game)
        b = board_from_solution(self.game, sol)
        self.assertTrue(self.game.check_horizontal(b))

    def test_next_solution(self):
        sol = ls_generate_initial(self.game)
        self.assertTrue(self.game.check_horizontal(board_from_solution(self.game, sol)))
        ls_generate_next(self.game, sol)
        self.assertTrue(self.game.check_horizontal(board_from_solution(self.game, sol)))


if __name__ == '__main__':
    unittest.main()
