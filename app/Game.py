"""Process all game data. Handles interfacing with the hidden state machine,
passing data to the right places, and returning the best move given a game dictionary."""

import random
from app.obj.Snake import Snake
from app.obj.Food import Food
from app.util.StateMachine import StateMachine
from app.util.Processor import Processor
from app.Board import Board


class Game:
    """
    World object has following top level attributes:

    weightGrid      (board)          - Board object
    width           (int)            - Board width
    height          (int)            - Board height
    you             (Snake)          - Snake object representing our snake
    food            (List<Point>     - List object containing an array of points
    turn            (int)            - 0-indexed int representing completed turns
    snakes          (List<Snake>)    - dict of Snake objects currently in play
    """

    def __init__(self, data):
        """
        Initialize the Game class.

        param1: dict - all data from /start POST.
        """
        self.width = data['width']
        self.height = data['height']
        self.board = Board(self.width, self.height)

        self.snakes = {}
        self.us = ''
        self.food = []
        self.turn = 0
        self.machine = None
        self.processor = None

    def firstMove(self, data):
        """
        Perform necessary actions upon receiving the first
        dictionary of the game

        param1: dictionary - all data from Battlesnake server.
        """
        for snake in data['snakes']['data']:
            snakeId = snake['id']
            self.snakes[snakeId] = Snake(snake)

        self.us = data['you']['id']
        self.food = Food(data['food'])
        self.machine = StateMachine(self.board, self.snakes, self.us, self.food)
        self.processor = Processor(self.board, self.snakes, self.us, self.food)

    def update(self, data):
        """
        Update game with current board from server.

        param1: dictionary - all data from Battlesnake server.
        """
        if data['turn'] is 0:
            self.firstMove(data)
            return

        # update all of our snakes
        for snake in data['snakes']['data']:
            snakeId = snake['id']
            self.snakes[snakeId].update(snake)

        self.food.update(data['food'])
        self.turn = data['turn']

    def getNextMove(self):
        """
        Use all algorithms to determine the next best move for our snake.
        """
        return 'up' # Remove this when Board.py is complete

        self.board.resetWeights()
        state = self.machine.getState()
        nextMove = []

        if state is 'IDLE':
            # run algorithms here
            pass
        elif state is 'HUNGRY':
            # eat food here
            pass
        elif state is 'TRAPPED':
            # be claustrophobic here
            pass
        elif state is 'STARVING':
            # stuff your face here
            pass
        elif state is 'CONFINED':
            # get out of here
            pass

        """
        THIS IS LEGACY CODE AND IS A CANDIDATE FOR REMOVAL

        self.processor.weightNotHitSnakes()
        self.processor.weightFood()
        self.processor.weightSmallSnakes()
        self.processor.weightLargeSnakes()

        self.board.setEdges()

        target = []
        ourSnake = self.snakes[self.us]

        priorityTarget = 0
        nodeValid = False

        while not nodeValid:
            topPriorityNode = self.board.getNodeWithPriority(priorityTarget)
            if self.board.isNodeWeightUnique(topPriorityNode):
                target = topPriorityNode
                priorityTarget += 1
            else:
                numDuplicates = self.board.countNodeWeightCopies(topPriorityNode)
                duplicateNodes = self.board.getNodesWithPriority(priorityTarget, \
                priorityTarget + numDuplicates - 1)
                closestLen = sys.maxsize
                closestPos = []

                for node in duplicateNodes:
                    tempPath = self.board.optimumPath(ourSnake.getHeadPosition(), node)
                    tempLen = len(tempPath)

                    if tempLen < closestLen and self.board.optimumPathLength(\
                    ourSnake.getHeadPosition(), node) != float('inf'):
                        closestLen = tempLen
                        closestPos = node

                priorityTarget += numDuplicates

                target = closestPos

            if target == []:
                nodeValid = False
            elif self.board.optimumPathLength(ourSnake.getHeadPosition(), target) != \
            float('inf'):
                nodeValid = True
        nextMove = self.processor.weightEnclosedSpaces(target)
        """

        return self.processor.nodeToDirection(nextMove, self.us)

    def getTaunt(self):
        """
        Return taunt for the move request.
        """
        taunts = ['Do you have any non-GMO food?', 'War. War never changes', 'Sssssslithering',\
         'Snakes? I hate snakes', 'Where can a snake get a bite to eat around here', 'up', 'down',\
          'left', 'right', 'Trying to catch garter snakes']

        return random.choice(taunts)
