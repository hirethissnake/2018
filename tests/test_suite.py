"""
Run all the tests available in this folder.
"""
import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = '.'
    #suite = loader.discover(start_dir)

    #this is temporary, as Board class is broken currently
    suite = unittest.TestSuite()
    for name in ['snake', 'food', 'main', 'statemachine']:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName('tests.test_' + name))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
