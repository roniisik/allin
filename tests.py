import unittest
from calc import *

class TestCalc(unittest.TestCase):
    def test_calc_deviation(self):
        data = [(0.74, '+'), (0.5, '-'), (0.5, '+'), (0.5, '+')]
        self.assertEqual(0.75, calc_deviation(data))


if __name__ == "__main__":
    unittest.main()