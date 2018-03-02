"""
Test state transitions, game operation.
"""

import unittest
from unittest.mock import Mock
from app.util.StateMachine import StateMachine

class TestStateMachine(unittest.TestCase):
    """
    Parent class to run unittests.
    """

    def setUp(self):
        """
        Create a fresh StateMachine object.
        """
        self.board = Mock()
        self.food = Mock()
        self.set = Mock()
        self.set.getConnectedToWall.return_value = [[0, 0]] * 100

        otherSnake = Mock()
        ourSnake = Mock()
        self.us = "glorious-us-uuid"
        self.snakes = {"mean-snake-uuid": otherSnake, self.us: ourSnake}

        self.machine = StateMachine(self.board, self.set, self.snakes, self.us, self.food)

    def test_initialization(self):
        """
        Ensure proper default state.
        """
        self.assertEqual(self.machine.state.name, "IDLE")
        self.assertEqual(self.machine.board, self.board)
        self.assertEqual(self.machine.us, self.us)
        self.assertEqual(self.machine.snakes, self.snakes)

    def test_set_and_recall_state(self):
        """
        Check if setting state corresponds to receiving that state.
        """
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
        ourSnake = self.snakes[self.us]
        ourSnake.getHealth.return_value = 50
        self.machine.step()
        self.assertEqual(self.machine.getState(), "HUNGRY")

        self.food.getPositions.return_value = [[0, 0]]
        ourSnake.getHealth.return_value = 30
        self.board.optimumPathLength.return_value = 40
        self.machine.step()
        self.assertEqual(self.machine.getState(), "STARVING")

        ourSnake.getSize.return_value = 5
        ourSnake.getHealth.return_value = 70
        self.machine.step()
        self.assertEqual(self.machine.getState(), "IDLE")

        ourSnake.getHealth.return_value = 50
        self.machine.step()
        self.assertEqual(self.machine.getState(), "HUNGRY")

        ourSnake.getHealth.return_value = 70
        self.machine.step()
        self.assertEqual(self.machine.getState(), "IDLE")

    def test_path_to_food_less(self):
        """
        Test pathToFoodLess(value) utility function.
        """
        ourSnake = self.snakes[self.us]

        self.board.optimumPathLength.return_value = 10
        self.food.getPositions.return_value = [[0, 0]] # these don't matter since optimumPathLength()
        ourSnake.getHeadPosition.return_value = [10, 0] # return value is constantly defined
        self.assertTrue(self.machine.pathToFoodLess(11))
        self.assertFalse(self.machine.pathToFoodLess(10))

        self.board.optimumPathLength.return_value = 1
        self.food.getPositions.return_value = [[0, 0], [0, 1], [0, 2]]
        self.assertTrue(self.machine.pathToFoodLess(2))


if __name__ == "__main__":
    unittest.main()
