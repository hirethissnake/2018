"""The brains of the operation. Maintains a persistant state that allows our snake to make
decisions based on a variety of factors in order to produce the optimal next move."""

from enum import Enum
from app.Snake import Snake
from app.Board import Board


class StateMachine:
    """The main state machine. Entry point for this file,
    and interface with Game class.

    Has following attributes:
    state           (State)         - State enum
    board           (Board)         - Board object
    otherSnakes     ({UUID:Snake})  - dict of UUIDs to Snake objects 
    us              (Snake)         - Snake object representing us"""

    def __init__(self, board, snakes, us):
        """Initialize the state machine.
        
        param1: Board - board object
        param2: {UUID:Snake} - dict mapping UUIDs to snakes
        param3: string - our snake's UUID 
        """
        self.state = State.IDLE
        self.board = board
        self.otherSnakes = dict(snakes) # perform shallow copy
        del self.otherSnakes[us]
        self.us = snakes[us]
        
    def getState(self):
        """
        Return the current state.

        return: string - enum name of current state
        """
        return self.state.name

    def setState(self, stateName):
        """
        Set the current state. Internal use only.

        param1: string - enum name of new state
        """
        self.state = State[stateName]

    def transition(self):
        """
        Use the available information to pick a new state.
        """
        currentState = self.getState()
        if currentState is "IDLE":
            print("we did it!")


class State(Enum):
    """Our state enumeration. Provides a consistent way to
    reference the list of available states."""

    IDLE = "we don't have any specific goal right now"
    HUNGRY = "we need to get some food soon"
    TRAPPED = "we are running out of space"
    STARVING = "we need food right away"
    CONFINED = "we need some serious maneuvering"
