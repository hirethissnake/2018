"""
Run all the tests available in this folder.
"""
import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
