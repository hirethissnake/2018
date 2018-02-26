"""
Test union and find operations.
"""

import unittest
from unittest.mock import Mock
from app.util.DisjointSet import DisjointSet
from app.Board import Board

class TestDisjointSet(unittest.TestCase):
    """
    Parent class to run unittests.
    """

    def setUp(self):
        """
        Create a fresh DisjointSet object.
        """
        self.board = Mock()
        self.board.getWidth.return_value = 20
        self.board.getHeight.return_value = 20

        self.set = DisjointSet(self.board)

    def test_initialization(self):
        """
        Ensure proper default state.
        """
        self.assertEqual(self.set.board, self.board)

    def test_update_all_or_nothing(self):
        """
        Ensure basic update is performed properly.
        """
        self.set.update()
        connected = self.set.getConnected([0, 0])
        for x in range(self.board.getWidth()):
            for y in range(self.board.getHeight()):
                self.assertTrue([x, y] in connected)
        
        self.board.getWeight.return_value = 0
        self.set.update()
        for x in range(self.board.getWidth()):
            for y in range(self.board.getHeight()):
                self.assertTrue(len(self.set.getConnected([x, y])) is 1)

    def test_update_real_board(self):
        """
        Ensure more complex features of update work.
        """
        board = Board(10, 10)
        dset = DisjointSet(self.board)
        board.setWeights([[0, 1], [1, 2], [2, 2], [3, 2], [3, 1], [4, 0]], 0) # disconnect top left

        dset.update()
        print(dset.getConnected([0,0]))



if __name__ == "__main__":
    unittest.main()
