"""
Test the Snake module & all its components.
"""
#!/usr/bin/python
import unittest
from app.Snake import Snake

class TestSnake(unittest.TestCase):
    """
    Parent class to run unittests.
    """

    def test_init(self):
        """
        Test the Snake init function.
        """
        initParams = {
            'id': 's1',
            'coords': [
                [0, 1],
                [1, 1]
            ],
            'health_points': 75
        }
        s1 = Snake(initParams)

        size_expected = len(initParams['coords'])
        state_expected = 'unknown'
        health_expected = initParams['health_points']
        headPosition_expected = initParams['coords'][0]
        tailPosition_expected = initParams['coords'][-1]
        positions_expected = initParams['coords']
        identifier_expected = initParams['id']

        self.assertEquals(s1.getSize(), size_expected)
        self.assertEqual(s1.getState(), state_expected)
        self.assertEqual(s1.getHealth(), health_expected)
        self.assertEqual(s1.getHeadPosition(), headPosition_expected)
        self.assertEqual(s1.getTailPosition(), tailPosition_expected)
        self.assertEqual(s1.getAllPositions(), positions_expected)
        self.assertEqual(s1.getIdentifier(), identifier_expected)

    def test_setState(self):
        """
        Test the setState function
        """
        initParams = {
            'id': 's1',
            'coords': [
                [0, 1],
                [1, 1]
            ],
            'health_points': 75
        }
        s1 = Snake(initParams)

        state_expected = 'food'
        s1.setState(state_expected)
        self.assertEqual(s1.getState(), state_expected)

        with self.assertRaises(ValueError):
            s1.setState('watermelon')

    def test_updates_valid(self):
        """
        Test valid updates.
        """
        initParams = {
            'id': 's1',
            'coords': [
                [0, 1],
                [1, 1],
                [1, 2]
            ],
            'health_points': 75
        }
        updateParams = {
            'coords': [
                [0, 0],
                [0, 1],
                [1, 1]
            ],
            'health_points': 65
        }

        s1 = Snake(initParams)
        s1.update(updateParams)

        headPosition_expected = updateParams['coords'][0]
        health_expected = updateParams['health_points']
        length_expected = len(updateParams['coords'])

        self.assertEqual(s1.getHeadPosition(), headPosition_expected)
        self.assertEqual(s1.getHealth(), health_expected)
        self.assertEqual(s1.getSize(), length_expected)

        updateParams = {
            'coords': [
                [1, 0],
                [0, 0],
                [0, 1],
                [1, 1]
            ],
            'health_points': 100
        }
        s1.update(updateParams)

        length_expected = len(updateParams['coords'])

        self.assertEqual(s1.getSize(), length_expected)

    def test_updates_invalid(self):
        """
        Test invalid updates.
        """
        initParams = {
            'id': 's1',
            'coords': [
                [0, 1],
                [1, 1],
                [1, 2]
            ],
            'health_points': 75
        }
        updateParams = {
            'coords': [
                [0, 0],
                [0, 1],
                [1, 1]
            ],
            'health_points': 'dog'
        }

        s1 = Snake(initParams)
        with self.assertRaises(ValueError):
            s1.update(updateParams)

if __name__ == "__main__":
    unittest.main()
