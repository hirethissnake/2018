"""Process all game data. Handles interfacing with the hidden state machine,
passing data to the right places, and returning the best move given a game dictionary."""

import random
import sys
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
        self.processor = Processor(self.board, self.snakes, self.us, self.food)
        self.weightSnakes()

    def update(self, data):
        """
        Update game with current board from server.

        param1: dictionary - all data from Battlesnake server.
        """
        if data['turn'] is 0:
            self.firstMove(data)
            return

        #for each snake obj from last turn
        toDel = []
        for snakeId in self.snakes:
            snakeFound = False

            #for each new snake obj
            for dataSnake in data['snakes']['data']:
                if dataSnake['id'] == snakeId:
                    #Update snake object
                    snakeFound = True
                    self.snakes[snakeId].update(dataSnake)

            if not snakeFound:
                toDel.append(snakeId)

        for snakeId in toDel:
            del self.snakes[snakeId]

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
        #state = self.machine.getState()
        state = 'IDLE'
        # Needs to be set to an [int, int]
        nextMove = []

        headPos = self.us.getHeadPosition()
        x, y = headPos
        surrounding = []

        if (x - 1) >= 0 and self.board.getWeight([x - 1, y]) != 0:
            surrounding.append([x - 1, y])
        if (x + 1) < self.board.width and self.board.getWeight([x + 1, y]) != 0:
            surrounding.append([x + 1, y])
        if (y + 1) < self.board.height and self.board.getWeight([x, y + 1]) != 0:
            surrounding.append([x, y + 1])
        if (y - 1) >= 0 and self.board.getWeight([x, y - 1]) != 0:
            surrounding.append([x, y - 1])

        try:
            if state is 'IDLE':
                #raise Exception('we hit a snag')
                headPos = self.us.getHeadPosition()

                # we have already weighted snakes, so make sure we don't
                # make a turn that will trap us

                x = headPos[0]
                y = headPos[1]
                surrounding = []

                if (x - 1) >= 0 and self.board.getWeight([x - 1, y]) != 0:
                    surrounding.append([x - 1, y])
                if (x + 1) < self.board.width and self.board.getWeight([x + 1, y]) != 0:
                    surrounding.append([x + 1, y])
                if (y + 1) < self.board.height and self.board.getWeight([x, y + 1]) != 0:
                    surrounding.append([x, y + 1])
                if (y - 1) >= 0 and self.board.getWeight([x, y - 1]) != 0:
                    surrounding.append([x, y - 1])

                maxSpaceCoords = []
                maxSpaceLen = 0
                for coord in surrounding:
                        
                    # due to IDLE state, there must be at least 1 non-wall node
                    weight = self.board.getWeight(coord)
                    if weight == 0:
                        continue

                    availableSpace = len(self.set.getConnectedToNode(coord))
                    if maxSpaceLen < availableSpace:
                        maxSpaceCoords = [coord]
                        maxSpaceLen = availableSpace
                    elif maxSpaceLen == availableSpace:
                        maxSpaceCoords.append(coord)

                # now we have a list of directions which will provide us with the
                # most maneuverability

                # reset weights around snake heads for path finding
                for _, snake in self.snakes.items():
                    if snake == self.us:
                        continue

                    surrounding = self.set.getSurrounding(snake.getHeadPosition())
                    if snake.getSize() < self.us.getSize():
                        for coord in surrounding:
                            if self.board.getWeight(coord) != 0:
                                self.board.setWeight(coord, 100)
                    else:
                        for coord in surrounding:
                            if self.board.getWeight(coord) != 0:
                                self.board.setWeight(coord, 1)
                self.set.update()

                # kill small snakes if they're there
                for coord in maxSpaceCoords:
                    if nextMove:
                        break
                    for _, snake in self.snakes.items():
                        if nextMove:
                            break
                        if snake != self.us and snake.getSize() < self.us.getSize():
                            otherHead = snake.getHeadPosition()
                            if self.set.pathExistsFromWall(otherHead, coord):
                                pathLen = self.board.optimumPathLength(headPos, otherHead)
                                if pathLen > -1 and pathLen < 3:
                                    nextMove = coord

                # if we have a move, return
                if nextMove:
                    return self.nodeToDirection(nextMove, self.us)

                # if we can trap a snake in one of these directions, let's slaughter 'em
                # this operation may be expensive, so we will have to check the times
                for coord in maxSpaceCoords:
                    # figure out which direction the coord represents
                    xDiff = coord[0] - headPos[0]
                    yDiff = coord[1] - headPos[1]

                    #Only worth attacking a snake if we are close to a wall
                    wallPath = []
                    if xDiff == -1: #left
                        try:
                            if self.set.pathExistsFromWall(headPos, [0, headPos[1]]):
                                wallPath = self.board.optimumPath(headPos, [0, headPos[1]])
                        except ValueError:
                            pass
                    if xDiff == 1: #right
                        try:
                            if self.set.pathExistsFromWall(headPos, [self.width - 1, headPos[1]]):
                                wallPath = self.board.optimumPath(headPos, [self.width - 1, headPos[1]])
                        except ValueError:
                            pass
                    if yDiff == -1: #up
                        try:
                            if self.set.pathExistsFromWall(headPos, [headPos[0], 0]):
                                wallPath = self.board.optimumPath(headPos, [headPos[0], 0])
                        except ValueError:
                            pass
                    if yDiff == 1: #down
                        try:
                            if self.set.pathExistsFromWall(headPos, [headPos[0], self.height - 1]):
                                wallPath = self.board.optimumPath(headPos, [headPos[0], self.height - 1])
                        except ValueError:
                            pass

                    # no path to wall in this direction, or too far
                    if not wallPath:
                        continue

                    wallPathLen = len(wallPath)
                    if wallPathLen > 3:
                        continue

                    # check how far we are from other snakes, and whether we can trap them
                    for _, snake in self.snakes.items():
                        if snake == self.us:
                            continue
                        otherHead = snake.getHeadPosition()
                        if self.set.pathExistsFromWall(otherHead, coord):
                            if self.board.optimumPathLength(headPos, otherHead) <= wallPathLen:
                                continue

                            # mock our snake taking this path, see if it traps the snake
                            weights = []
                            for wallCoord in wallPath:
                                weights.append(self.board.getWeight(wallCoord))
                                self.board.setWeight(wallCoord, 0)
                            self.set.update()

                            # if we can likely trap it
                            if len(self.set.getConnectedToWall(otherHead)) < self.us.getSize():
                                nextMove = coord

                            # reset the board weights
                            for i in range(wallPathLen):
                                self.board.setWeight(wallPath[i], weights[i])
                            self.set.update()
                        
                    # we have found a trapping move
                    if not nextMove:
                        break

                if nextMove:
                    return self.nodeToDirection(nextMove, self.us)

                self.board.setWeight(headPos, 0)

                # we did not find a trapping move, find food
                foodList = self.food.getPositions()
                closestFoodDistance = sys.maxsize
                closestFoodPath = None
                print(maxSpaceCoords)
                for coord in maxSpaceCoords:
                    for food in foodList:
                        if self.board.getWeight(food) != 0 and not nextMove:
                            if coord == food:
                                nextMove = food
                                return self.nodeToDirection(nextMove, self.us)

                            if self.set.pathExistsFromNode(coord, food):
                                path = self.board.optimumPath(coord, food)
                                pathLen = 0
                                if path != None:
                                    pathLen = len(path)
                                if pathLen < closestFoodDistance:
                                    closestFoodDistance = pathLen
                                    closestFoodPath = path
                
                if closestFoodPath is None:
                    nextMove = maxSpaceCoords[0]
                else:
                    nextMove = closestFoodPath[0]
                print(nextMove)

                return self.nodeToDirection(nextMove, self.us)

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
        except Exception as e:
            print(e, e.__traceback__)
            print('Oh FRIDGE!! getNextMove had an ERROR!!??!!\n Picking a heuristic best move.\n')
            allSnakes = []
            for snakeID in self.snakes:
                allSnakes.append(self.snakes[snakeID].getAllPositions())
            for coord in surrounding:
                if coord not in allSnakes:
                    nextMove = coord
                    break
            print('Move: {}, direction: {}'.format(nextMove, self.nodeToDirection(nextMove, self.us)))
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
