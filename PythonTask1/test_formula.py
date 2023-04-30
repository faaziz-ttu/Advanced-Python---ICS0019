import unittest
from square_faaziz.square_formula import SquareFunction

class TestSquareFormula(unittest.TestCase):
    def test_square_formula(self):
        self.assertEqual(SquareFunction().square_form(2, 3), 25)
        self.assertEqual(SquareFunction().square_form(-4, -2), 36)
        self.assertEqual(SquareFunction().square_form(0, 0), 0)
        self.assertEqual(SquareFunction().square_form(10, 0), 100)
        self.assertEqual(SquareFunction().square_form(-5, 5), 0)

if __name__ == '__main__':
    unittest.main()