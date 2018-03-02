"""
Run all the tests available in this folder.
"""
import unittest
import sys

if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir)

    # Force high verbosity and hide internal prints during tests
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())
