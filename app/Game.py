"""Process all game data. Handles interfacing with the hidden state machine,
passing data to the right places, and returning the best move given a game dictionary."""

import random
from app.obj.Snake import Snake
from app.obj.Food import Food
from app.util.StateMachine import StateMachine
from app.util.Processor import Processor
from app.util.DisjointSet import DisjointSet
from app.Board import Board


class Game:
    """
    World object has following top level attributes:

    weightGrid      (board)          - Board object
    width           (int)            - Board width
    height          (int)            - Board height
    you             (Snake)          - Snake object representing our snake
    food            (List<Point>]     - List object containing an array of points
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
        self.us = None
        self.usName = ''
        self.food = None
        self.turn = 0
        self.set = None
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

        self.usName = data['you']['id']
        self.us = self.snakes[self.usName]
        self.food = Food(data['food'])
        self.set = DisjointSet(self.board)
        self.machine = StateMachine(self.board, self.set, self.snakes, self.us, self.food)
        self.processor = Processor(self.board, self.set, self.snakes, self.us, self.food)
        self.weightSnakes()

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
        self.weightSnakes()

    def weightSnakes(self):
        """
        Perform state-independent weighting of snake bodies. If a specific state requires
        different waiting of snake heads or tails, then they may perform weighting manually.
        """
        self.board.resetWeights()

        for _, snake in self.snakes.items():
            self.board.setWeights(snake.getAllPositions(), 0)
            if snake != self.us and snake.getSize() < self.us.getSize():
                self.board.setWeights(self.set.getSurrounding(snake.getHeadPosition()), 0)

        self.set.update()

    def getTaunt(self):
        """
        Return taunt for the move request.
        """
        taunts = ['Do you have any non-GMO food?', 'War. War never changes', 'Sssssslithering',\
         'Snakes? I hate snakes', 'Where can a snake get a bite to eat around here', 'up', 'down',\
          'left', 'right', 'Trying to catch garter snakes']

        return random.choice(taunts)

    def getNextMove(self):
        """
        Use all algorithms to determine the next best move for our snake.
        """
        state = self.machine.getState()

        # Needs to be set to an [int, int]
        nextMove = [0, 0]
        state = 'TRAPPED'
        if state is 'IDLE':
            # run algorithms here
            pass
        elif state is 'HUNGRY':
            # eat food here
            pass
        elif state is 'TRAPPED':
            oursnake = self.us
            current_pos = oursnake.getHeadPosition()
            goal = self.processor.getFarthestLocationTrapped(current_pos)
            path = self.board.optimumPath(current_pos, goal)
            for i in range(len(path)-1):
                path = self.processor.extendPath(path,path[i],path[i+1],i)
            nextMove = path[1]
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
        direction = self.nodeToDirection(nextMove, self.us)
        return direction

    def nodeToDirection(self, node, snake):
        """
        Convert a coord array into an up, down, left, right direction.
        param1: [int,int] - x,y coords of a node.
        param2: Snake - snake in the game (ie, in snakes{})

        Raises: ValueError
            if: node is not adjacent to the snakes head

        return: string - direction to go
        """
        head = snake.getHeadPosition()

        if node[0] == (head[0] + 1):
            return 'right'
        if node[0] == (head[0] - 1):
            return 'left'
        if node[1] == (head[1] + 1):
            return 'down'
        if node[1] == (head[1] - 1):
            return 'up'
        else:
            raise ValueError('node must be adjacent')
