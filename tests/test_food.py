"""
Test the Food module & all its components.
"""
#!/usr/bin/python
import unittest
from app.Food import Food

class TestSnake(unittest.TestCase):
    """
    Parent class to run unittests.
    """

    def setUp(self):
        """
        Create a fresh Food object.
        """
        self.food = Food([])

    def test_init(self):
        """
        Test the Food init function.
        """
        self.assertEqual(self.food.getPositions(), [])

        self.food = Food([[1, 1], [2, 2]])
        self.assertEqual(self.food.getPositions(), [[1, 1], [2, 2]])

        self.food = Food([[]])
        self.assertEqual(self.food.getPositions(), [[]])

    def test_update(self):
        """
        Test the Food update function.
        """
        self.food.update([[0, 0]])
        self.assertEqual(self.food.getPositions(), [[0, 0]])
        self.food.update([[2, 2]])
        self.assertEqual(self.food.getPositions(), [[2, 2]])
        self.food.update([[0, 0], [1, 1], [2, 2], [3, 3]])
        self.assertEqual(self.food.getPositions(), [[0, 0], [1, 1], [2, 2], [3, 3]])


if __name__ == "__main__":
    unittest.main()
