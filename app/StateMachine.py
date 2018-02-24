"""The brains of the operation. Maintains a persistant state that allows our snake to make
decisions based on a variety of factors in order to produce the optimal next move."""

from enum import Enum
from app.Snake import Snake
from app.Board import Board


class StateMachine:
    """The main state machine. Entry point for this file,
    and interface with Game class.

    Has following attributes:
    TODO          (board)     - Board object"""

    def __init__(self):
        """Initialize the state machine."""
        self.state = State.IDLE

    def getState(self):
        """
        Return the current state.

        return: string - enum name of current state
        """
        return self.state.name

    def setState(self, stateName):
        """
        Set the current state.

        param1: string - enum name of new state
        """
        self.state = State[stateName]

class State(Enum):
    """Our state enumeration. Provides a consistent way to
    reference the list of available states."""

    IDLE = "we don't have any specific goal right now"
    HUNGRY = "we need to get some food soon"
    TRAPPED = "we are running out of space"
    STARVING = "we need food right away"
    CONFINED = "we need some serious maneuvering"
