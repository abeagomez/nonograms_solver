import unittest
from bitset import Bitset


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


if __name__ == '__main__':
    unittest.main()
