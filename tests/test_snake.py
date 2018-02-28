"""
Test the Snake module & all its components.
"""
#!/usr/bin/python
import unittest
from app.obj.Snake import Snake

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
            'length': 2,
            'body': {
                'object': 'list',
                'data': [
                    {
                        'object': 'point',
                        'x': 0,
                        'y': 1
                    },
                    {
                        'object': 'point',
                        'x': 1,
                        'y': 1
                    }
                ]
            },
            'health': 75
        }
        s1 = Snake(initParams)
        initParams['body']['data'] = list(map(lambda point: [point['x'], point['y']], initParams['body']['data']))

        size_expected = len(initParams['body']['data'])
        health_expected = initParams['health']
        headPosition_expected = initParams['body']['data'][0]
        tailPosition_expected = initParams['body']['data'][-1]
        positions_expected = initParams['body']['data']
        identifier_expected = initParams['id']

        self.assertEqual(s1.getSize(), size_expected)
        self.assertEqual(s1.getHealth(), health_expected)
        self.assertEqual(s1.getHeadPosition(), headPosition_expected)
        self.assertEqual(s1.getTailPosition(), tailPosition_expected)
        self.assertEqual(s1.getAllPositions(), positions_expected)
        self.assertEqual(s1.getIdentifier(), identifier_expected)

    def test_updates_valid(self):
        """
        Test valid updates.
        """
        initParams = {
            'id': 's1',
            'length': 3,
            'body': {
                'object': 'list',
                'data': [
                    {
                        'object': 'point',
                        'x': 0,
                        'y': 1
                    },
                    {
                        'object': 'point',
                        'x': 1,
                        'y': 1
                    },
                    {
                        'object': 'point',
                        'x': 1,
                        'y': 2
                    }
                ]
            },
            'health': 75
        }
        updateParams = {
            'body': {
                'object': 'list',
                'data': [
                    {
                        'object': 'point',
                        'x': 0,
                        'y': 0
                    },
                    {
                        'object': 'point',
                        'x': 0,
                        'y': 1
                    },
                    {
                        'object': 'point',
                        'x': 1,
                        'y': 1
                    }
                ]
            },
            'length': 3,
            'health': 65
        }

        s1 = Snake(initParams)
        s1.update(updateParams)
        initParams['body']['data'] = list(map(lambda point: [point['x'], point['y']], initParams['body']['data']))
        updateParams['body']['data'] = list(map(lambda point: [point['x'], point['y']], updateParams['body']['data']))

        headPosition_expected = updateParams['body']['data'][0]
        tailPosition_expected = updateParams['body']['data'][-1]
        positions_expected = updateParams['body']['data']
        health_expected = updateParams['health']
        length_expected = len(updateParams['body']['data'])

        self.assertEqual(s1.getHeadPosition(), headPosition_expected)
        self.assertEqual(s1.getHealth(), health_expected)
        self.assertEqual(s1.getSize(), length_expected)
        self.assertEqual(s1.getTailPosition(), tailPosition_expected)
        self.assertEqual(s1.getAllPositions(), positions_expected)

        updateParams = {
            'body': {
                'object': 'list',
                'data': [
                    {
                        'object': 'point',
                        'x': 1,
                        'y': 0
                    },
                    {
                        'object': 'point',
                        'x': 0,
                        'y': 0
                    },
                    {
                        'object': 'point',
                        'x': 0,
                        'y': 1
                    },
                    {
                        'object': 'point',
                        'x': 1,
                        'y': 1
                    },
                ]
            },
            'length': 4,
            'health': 100
        }

        s1.update(updateParams)
        updateParams['body']['data'] = list(map(lambda point: [point['x'], point['y']], updateParams['body']['data']))

        length_expected = len(updateParams['body']['data'])

        self.assertEqual(s1.getSize(), length_expected)

    def test_updates_invalid(self):
        """
        Test invalid updates.
        """
        initParams = {
            'id': 's1',
            'body': {
                'object': 'list',
                'data': [
                    {
                        'object': 'point',
                        'x': 0,
                        'y': 1
                    },
                    {
                        'object': 'point',
                        'x': 1,
                        'y': 1
                    },
                    {
                        'object': 'point',
                        'x': 1,
                        'y': 2
                    }
                ]
            },
            'length': 3,
            'health': 75
        }
        updateParams = {
            'body': {
                'object': 'list',
                'data': [
                    {
                        'object': 'point',
                        'x': 0,
                        'y': 0
                    },
                    {
                        'object': 'point',
                        'x': 0,
                        'y': 1
                    },
                    {
                        'object': 'point',
                        'x': 1,
                        'y': 1
                    }
                ]
            },
            'length': 3,
            'health': 'dog'
        }

        s1 = Snake(initParams)
        with self.assertRaises(TypeError):
            s1.update(updateParams)

if __name__ == "__main__":
    unittest.main()
