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
        param4: [[x,y]] - list of food coordinates
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

    def step(self):
        """
        Use the available information to pick a new state.
        """
        size = self.us.getSize()
        health = self.us.getHealth()

        currentState = self.getState()
        if currentState is "IDLE":
            if self.snakeHealthLess(60):
                self.setState("HUNGRY")
            elif self.availableSpaceLess(2 * size):
                self.setState("CONFINED")
            elif self.availableSpaceLess(3 * size):
                self.setState("TRAPPED")
        elif currentState is "HUNGRY":
            if not self.pathToFoodLess(health + 10) \
                    or self.snakeHealthLess(15):
                self.setState("STARVING")
            elif self.availableSpaceLess(1.5 * size):
                self.setState("CONFINED")
            elif self.availableSpaceLess(2.5 * size):
                self.setState("TRAPPED")
            elif not self.snakeHealthLess(60):
                self.setState("IDLE")
        elif currentState is "TRAPPED":
            if not self.pathToFoodLess(health + 5) \
                    or self.snakeHealthLess(15):
                self.setState("STARVING")
            elif not self.availableSpaceLess(4 * size) and self.snakeHealthLess(60):
                self.setState("HUNGRY")
            elif self.availableSpaceLess(1.5 * size):
                self.setState("CONFINED")
            elif not self.availableSpaceLess(4 * size) and not self.snakeHealthLess(60):
                self.setState("IDLE")
        elif currentState is "STARVING":
            if not self.snakeHealthLess(40) and self.availableSpaceLess(3 * size):
                self.setState("TRAPPED")
            elif (self.availableSpaceLess(1.5 * size) and not self.snakeHealthLess(10) and not self.pathToFoodLess(health)) \
                    or self.availableSpaceLess(size):
                self.setState("CONFINED")
            elif not self.snakeHealthLess(60):
                self.setState("IDLE")
        elif currentState is "CONFINED":
            if self.snakeHealthLess(10) and not self.availableSpaceLess(size):
                self.setState("STARVING")
            elif not self.availableSpaceLess(4 * size) and self.snakeHealthLess(50):
                self.setState("HUNGRY")
            elif not self.availableSpaceLess(2.5 * size) and self.availableSpaceLess(4 * size):
                self.setState("TRAPPED")
            elif not self.availableSpaceLess(4 * size) and not self.snakeHealthLess(60):
                self.setState("IDLE")

    def snakeHealthLess(self, value):
        """
        Determine if a snake has health lower than 'value'

        param1: Snake - snake to retrieve health from
        param2: int - value to compare against
        return: boolean - True if health less than 'value'
        """
        return self.us.getHealth() < value

    def pathToFoodLess(self, value):
        """
        Determine if a snake is closer than 'value' squares from food

        param1: Snake - snake to retrieve position from
        param2: value - value to compare against
        return: boolean - True if 'snake' is closer than 'value'
        """
        return True

    def availableSpaceLess(self, value):
        """
        Determine if a snake has health lower than 'value'

        param1: Snake - snake to retrieve position from
        param2: value - value to compare against
        return: boolean - True if health less than 'value'
        """
        return True


class State(Enum):
    """Our state enumeration. Provides a consistent way to
    reference the list of available states."""

    IDLE = "we don't have any specific goal right now"
    HUNGRY = "we need to get some food soon"
    TRAPPED = "we are running out of space"
    STARVING = "we need food right away"
    CONFINED = "we need some serious maneuvering"
