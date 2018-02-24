"""
Test state transitions, game operation.
"""

import unittest
from unittest.mock import MagicMock
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
        self.board = MagicMock()

        otherSnake = {'length': 3}
        us = {'length': 3}        
        self.snakes = {'mean-snake-uuid': otherSnake, 'glorious-us-uuid': us}

        self.machine = StateMachine(self.board, self.snakes, "glorious-us-uuid")

    def test_initialization(self):
        """
        Ensure proper default state.
        """
        self.assertEqual(self.machine.getState(), "IDLE")
        self.assertEqual(self.machine.board, self.board)
        self.assertEqual(self.machine.us, self.snakes['glorious-us-uuid'])
        del self.snakes['glorious-us-uuid']
        self.assertEqual(self.machine.otherSnakes, self.snakes)

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

    def test_transition(self):
        """
        Make sure you cannot set an invalid state.
        """
        self.machine.transition()


if __name__ == "__main__":
    unittest.main()
