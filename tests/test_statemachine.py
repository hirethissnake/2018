"""
Test state transitions, game operation.
"""

import unittest
from unittest.mock import Mock
from app.StateMachine import StateMachine
from app.Board import Board
from app.Snake import Snake


class TestStateMachine(unittest.TestCase):
    """
    Parent class to run unittests.
    """

    def setUp(self):
        """
        Create a fresh StateMachine object.
        """
        self.board = Mock()
        self.otherSnake = Mock()
        self.us = Mock()
        self.food = Mock()
        snakes = {'mean-snake-uuid': self.otherSnake, 'glorious-us-uuid': self.us}

        self.machine = StateMachine(self.board, snakes, "glorious-us-uuid", self.food)

    def test_initialization(self):
        """
        Ensure proper default state.
        """
        self.assertEqual(self.machine.state.name, "IDLE")
        self.assertEqual(self.machine.board, self.board)
        self.assertEqual(self.machine.us, self.us)
        self.assertEqual(self.machine.otherSnakes, {'mean-snake-uuid': self.otherSnake})

    def test_set_and_recall_state(self):
        """
        Check if setting state corresponds to receiving that state.
        """
        for _ in range(5):
            self.machine.setState("HUNGRY")
            self.assertEqual(self.machine.getState(), "HUNGRY")
            self.machine.setState("TRAPPED")
            self.assertEqual(self.machine.getState(), "TRAPPED")
            self.machine.setState("STARVING")
            self.assertEqual(self.machine.getState(), "STARVING")
            self.machine.setState("IDLE")
            self.assertEqual(self.machine.getState(), "IDLE")
            self.machine.setState("CONFINED")
            self.assertEqual(self.machine.getState(), "CONFINED")
            self.machine.setState("HUNGRY")
            self.machine.setState("HUNGRY")
            self.machine.setState("IDLE")
            self.assertEqual(self.machine.getState(), "IDLE")

    def test_set_invalid_state(self):
        """
        Make sure you cannot set an invalid state.
        """
        self.assertRaises(KeyError, self.machine.setState, "INVALID")
        self.assertRaises(KeyError, self.machine.setState, 2)

    def test_transition(self): # TODO
        """
        Test transitioning between states based.
        """
        self.us.getSize.return_value = 3
        self.us.getHealth.return_value = 100
        self.us.getHeadPosition.return_value = [1, 1]
        self.food.getPositions.return_value = [[0, 0]]

        self.machine.step()
        self.assertEqual(self.machine.getState(), "CONFINED")

    def test_path_to_food_less(self):
        """
        Test pathToFoodLess(value) utility function.
        """
        self.board.optimumPathLength.return_value = 10
        self.food.getPositions.return_value = [[0, 0]] # these don't matter since optimumPathLength()
        self.us.getHeadPosition.return_value = [10, 0] # return value is constantly defined
        self.assertTrue(self.machine.pathToFoodLess(11))
        self.assertFalse(self.machine.pathToFoodLess(10))

        self.board.optimumPathLength.return_value = 1
        self.food.getPositions.return_value = [[0, 0], [0, 1], [0, 2]]
        self.assertTrue(self.machine.pathToFoodLess(2))


if __name__ == "__main__":
    unittest.main()
