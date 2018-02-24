"""
Test state transitions, game operation.
"""

import unittest
from app.StateMachine import StateMachine


class TestStateMachine(unittest.TestCase):
    """
    Parent class to run unittests.
    """

    def setUp(self):
        """
        Create a fresh StateMachine object.
        """
        self.machine = StateMachine()

    def test_initialization(self):
        """
        Ensure proper default state.
        """
        self.assertEqual(self.machine.getState(), "IDLE")

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


if __name__ == "__main__":
    unittest.main()
