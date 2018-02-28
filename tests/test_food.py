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
                    {
                        'object': 'point',
                        'x': 1,
                        'y': 1
                    },
                    {
                        'object': 'point',
                        'x': 2,
                        'y': 2
                    }
                ]
            }
        }

        self.food.update(world['food'])
        world['food']['data'] = list(map(lambda point: [point['x'], point['y']], world['food']['data']))
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
                    {
                        'object': 'point',
                        'x': 0,
                        'y': 0
                    }
                ]
            }
        }
        world2 = {
            'object': 'world',
            'food': {
                'object': 'list',
                'data': [
                    {
                        'object': 'point',
                        'x': 2,
                        'y': 2
                    }
                ]
            }
        }
        world3 = {
            'object': 'world',
            'food': {
                'object': 'list',
                'data': [
                    {
                        'object': 'point',
                        'x': 0,
                        'y': 0
                    },
                    {
                        'object': 'point',
                        'x': 1,
                        'y': 1
                    },
                    {
                        'object': 'point',
                        'x': 2,
                        'y': 2
                    },
                    {
                        'object': 'point',
                        'x': 3,
                        'y': 3
                    },
                ]
            }
        }
        self.food.update(world1['food'])
        world1['food']['data'] = list(map(lambda point: [point['x'], point['y']], world1['food']['data']))
        self.assertEqual(self.food.getPositions(), world1['food']['data'])
        self.food.update(world2['food'])
        world2['food']['data'] = list(map(lambda point: [point['x'], point['y']], world2['food']['data']))
        self.assertEqual(self.food.getPositions(), world2['food']['data'])
        self.food.update(world3['food'])
        world3['food']['data'] = list(map(lambda point: [point['x'], point['y']], world3['food']['data']))
        self.assertEqual(self.food.getPositions(), world3['food']['data'])


if __name__ == '__main__':
    unittest.main()
