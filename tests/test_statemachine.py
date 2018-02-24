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
        Create a fresh StateMachine object
        """
        self.machine = StateMachine()

    def test_initialization(self):
        """
        Ensure proper default state
        """
        self.assertEqual(self.machine.getState(), "IDLE")


if __name__ == "__main__":
    unittest.main()
