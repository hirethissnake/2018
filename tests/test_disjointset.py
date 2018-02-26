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
        self.board = Mock(width=20, height=20)

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
        for x in range(self.board.width):
            for y in range(self.board.width):
                self.assertTrue([x, y] in connected)
        
        self.board.getWeight.return_value = 0
        self.set.update()
        for x in range(self.board.width):
            for y in range(self.board.height):
                self.assertTrue(len(self.set.getConnected([x, y])), 1)

    def test_update_real_board(self):
        """
        Ensure more complex features of update work.
        """
        board = Board(10, 10)
        dset = DisjointSet(board)
        enclosedSpace = [[0, 0], [1, 0], [1, 1], [2, 0], [2, 1], [3, 0]]
        wall = [[0, 1], [1, 2], [2, 2], [3, 2], [3, 1], [4, 0]]
        
        board.setWeights(wall, 0) # disconnect top left

        dset.update()
        self.assertEqual(sorted(dset.getConnected([0,0])), enclosedSpace)

        for x in range(board.width):
            for y in range(board.height):
                if [x, y] not in enclosedSpace:
                    for coord in enclosedSpace:
                        self.assertFalse(dset.areConnected(coord, [x, y]))

        for coord1 in enclosedSpace:
            for coord2 in enclosedSpace:
                self.assertTrue(dset.areConnected(coord1, coord2))


if __name__ == "__main__":
    unittest.main()
