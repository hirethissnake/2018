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
        snakes = {'mean-snake-uuid': self.otherSnake, 'glorious-us-uuid': self.us}

        self.machine = StateMachine(self.board, snakes, "glorious-us-uuid")

    def test_initialization(self):
        """
        Ensure proper default state.
        """
        self.assertEqual(self.machine.getState(), "IDLE")
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

    def test_transition(self):
        """
        Test transitioning between states based.
        """
        self.us.getSize.return_value = 3
        self.us.getHealth.return_value = 100
        
        self.machine.step()
        self.assertEqual(self.machine.getState(), "CONFINED")


if __name__ == "__main__":
    unittest.main()
