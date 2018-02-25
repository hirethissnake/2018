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
    us              (Snake)         - Snake object representing us
    food            (Food)          - Food object representing food coordinates"""

    def __init__(self, board, snakes, us, food):
        """
        Initialize the state machine.
        
        param1: Board - board object
        param2: {UUID:Snake} - dict mapping UUIDs to snakes
        param3: string - our snake's UUID 
        param4: [[x,y]] - list of food coordinates
        """
        self.state = State.IDLE
        self.board = board
        self.snakes = snakes
        self.us = us
        self.food = food
        
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
        ourSnake = self.snakes[self.us]
        size = ourSnake.getSize()
        health = ourSnake.getHealth()

        currentState = self.getState()
        if currentState is "IDLE":
            if health < 60:
                self.setState("HUNGRY")
            elif self.availableSpaceLess(2 * size):
                self.setState("CONFINED")
            elif self.availableSpaceLess(3 * size):
                self.setState("TRAPPED")
        elif currentState is "HUNGRY":
            if not self.pathToFoodLess(health + 10) \
                    or health < 15:
                self.setState("STARVING")
            elif self.availableSpaceLess(1.5 * size):
                self.setState("CONFINED")
            elif self.availableSpaceLess(2.5 * size):
                self.setState("TRAPPED")
            elif health > 60:
                self.setState("IDLE")
        elif currentState is "TRAPPED":
            if not self.pathToFoodLess(health + 5) \
                    or health < 15:
                self.setState("STARVING")
            elif not self.availableSpaceLess(4 * size) and health > 60:
                self.setState("HUNGRY")
            elif self.availableSpaceLess(1.5 * size):
                self.setState("CONFINED")
            elif not self.availableSpaceLess(4 * size) and health > 60:
                self.setState("IDLE")
        elif currentState is "STARVING":
            if health > 40 and self.availableSpaceLess(3 * size):
                self.setState("TRAPPED")
            elif (self.availableSpaceLess(1.5 * size) and health > 10 and not self.pathToFoodLess(health)) \
                    or self.availableSpaceLess(size):
                self.setState("CONFINED")
            elif health > 60:
                self.setState("IDLE")
        elif currentState is "CONFINED":
            if health < 10 and not self.availableSpaceLess(size):
                self.setState("STARVING")
            elif not self.availableSpaceLess(4 * size) and health < 50:
                self.setState("HUNGRY")
            elif not self.availableSpaceLess(2.5 * size) and self.availableSpaceLess(4 * size):
                self.setState("TRAPPED")
            elif not self.availableSpaceLess(4 * size) and health > 60:
                self.setState("IDLE")

    def pathToFoodLess(self, value):
        """
        Determine if a snake is closer than 'value' squares from food

        param1: value - value to compare against
        return: boolean - True if 'snake' is closer than 'value'
        """
        ourSnake = self.snakes[self.us]
        headPos = ourSnake.getHeadPosition()
        for pos in self.food.getPositions():
            distance = self.board.optimumPathLength(pos, headPos)
            if distance < value:
                return True
        return False

    def availableSpaceLess(self, value):
        """
        Determine if a snake has health lower than 'value'

        param1: value - value to compare against
        return: boolean - True if health less than 'value'
        """
        return False


class State(Enum):
    """Our state enumeration. Provides a consistent way to
    reference the list of available states."""

    IDLE = "we don't have any specific goal right now"
    HUNGRY = "we need to get some food soon"
    TRAPPED = "we are running out of space"
    STARVING = "we need food right away"
    CONFINED = "we need some serious maneuvering"
