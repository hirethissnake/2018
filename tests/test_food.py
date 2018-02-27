"""
Test the Food module & all its components.
"""
#!/usr/bin/python
import unittest
from app.obj.Food import Food

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
        self.assertEqual(self.food.getPositions(), [[]])

        world = {
            'object': 'world',
            'food': {
                'object': 'list',
                'data': [
                    [1, 1], [2, 2]
                ]
            }
        }

        self.food = Food(world['food'])
        self.assertEqual(self.food.getPositions(), world['food']['data'])

        self.food = Food([[]])
        self.assertEqual(self.food.getPositions(), [[]])

    def test_update(self):
        """
        Test the Food update function.
        """

        world1 = {
            'object': 'world',
            'food': {
                'object': 'list',
                'data': [
                    [0, 0]
                ]
            }
        }
        world2 = {
            'object': 'world',
            'food': {
                'object': 'list',
                'data': [
                    [2, 2]
                ]
            }
        }
        world3 = {
            'object': 'world',
            'food': {
                'object': 'list',
                'data': [
                    [0, 0], [1, 1], [2, 2], [3, 3]
                ]
            }
        }
        self.food.update(world1['food'])
        self.assertEqual(self.food.getPositions(), world1['food']['data'])
        self.food.update(world2['food'])
        self.assertEqual(self.food.getPositions(), world2['food']['data'])
        self.food.update(world3['food'])
        self.assertEqual(self.food.getPositions(), world3['food']['data'])


if __name__ == '__main__':
    unittest.main()
