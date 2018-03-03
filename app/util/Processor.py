"""Performs grunt work algorithms for decision processing."""

import sys

class Processor:
    """The main state machine. Entry point for this file,
    and interface with Game class.

    Has following attributes:
    board           Board           - Board object
    width           int             - width of the Board object
    height          int             - height of the Board object
    snakes          {UUID:Snake}    - dict of UUIDs to Snake objects 
    us              UUID            - The UUID of our snake
    food            Food            - Food object representing food coordinates
    """

    def __init__(self, board, set, snakes, us, food):
        """
        Initialize the processor.
        
        param1: Board - board object
        param2: {UUID:Snake} - dict mapping UUIDs to snakes
        param3: string - our snake's UUID 
        param4: [[x,y]] - list of food coordinates
        """
        self.board = board
        self.width = board.width
        self.height = board.height
        self.set = set
        self.snakes = snakes
        self.us = us
        
        self.food = food

    def weightNotHitSnakes(self):
        """Weight grid to avoid snake hitting other snakes and itself."""
        # pylint: disable=E1121

        for s in self.snakes:
            positions = self.snakes[s].getAllPositions()
            head = positions[0]
            tail = positions[-1]
            self.board.setWeights(positions, 0.0)
            self.board.setWeight(tail, 50.0)

            # if snake could eat food, avoid the tail
            # above by 1
            if (head[1]) > 0 and [head[0], head[1] - 1] in self.food:
                self.board.setWeight(tail, 0.0)
            # left by 1
            if (head[0]) < self.width-1 and [head[0] + 1, head[1]] in self.food:
                self.board.setWeight(tail, 0.0)
            # right by 1
            if (head[0]) > 0 and [head[0] - 1, head[1]] in self.food:
                self.board.setWeight(tail, 0.0)
            # below
            if (head[1]) < self.height-1 and [head[0], head[1] + 1] in self.food:
                self.board.setWeight(tail, 0.0)

    def weightFood(self):
        """Weight grid with food necessity"""
        #TODO
        #How desperately do we need food
        #Goes through all food and returns the closest according to optimumPath

        pathLength = 500
        shortestPath = sys.maxsize
        oursnake = self.snakes[self.us]
        head = oursnake.getHeadPosition()
        # health = oursnake.getHealth()
        for foodCoords in self.food:
            pathLength = len(self.board.optimumPath(head, foodCoords))
            if pathLength < shortestPath:
                shortestPath = pathLength
                #closestFoodCoord = foodCoords

            #foodCoord += 1
            # this will change based on health decrementation
            foodWeight = 100 # - health - pathLength
            self.board.setWeight(foodCoords, foodWeight)

    def weightSmallSnakes(self):
        """Positively weight smaller snakes for murdering purposes"""
        #TODO
        #Compare size
        #How long will it take to get to the snake?
        #How much food is around for the snake to grow?
        oursnake = self.snakes[self.us]
        ourSize = oursnake.getSize()
        weightAdd = 0

        for otherSnake in self.snakes:
            if otherSnake != self.us:
                otherSnakeSize = self.snakes[otherSnake].getSize()
                if  otherSnakeSize < ourSize:
                    # Run this code for every snake on the board that's
                    # not you AND smaller than you
                    headA = self.headArea(self.snakes[otherSnake])
                    #this algorithm could be altered to add varying values not just a blanket range
                    weightAdd = 12
                    for headCoord in headA:
                        self.board.addWeight(headCoord, weightAdd)

    def headArea(self, snake):
        """Return an area around the head so that it can be weighted
        param1: snake whose head area needs to be evaluated"""

        #TODO
        #find head
        #find area
        #find body
        #return coordinates
        head = snake.getHeadPosition()
        xCoord = head[0]
        yCoord = head[1]
        upperBoundX = xCoord+2
        upperBoundY = yCoord+2
        lowerBoundX = xCoord-2
        lowerBoundY = yCoord-2
        newCoordinates = []
        if upperBoundY >= self.height:
            upperBoundY = self.height-1
        if upperBoundX >= self.width:
            upperBoundX = self.width-1
        if lowerBoundY < 0:
            lowerBoundY = 0
        if lowerBoundX < 0:
            lowerBoundX = 0
        #goes through a 5x5 grid around the snake and creates an array of those coordinates
        for xCoordNew in range(lowerBoundX, upperBoundX+1):
            for yCoordNew in range(lowerBoundY, upperBoundY+1):
                newCoordinates.append([xCoordNew, yCoordNew])
        #removes any body segments from the grid
        for otherSnakes in self.snakes:
            for bodySegment in self.snakes[otherSnakes].getAllPositions():
                #Run this code for all body (and head) segments of all snakes
                if bodySegment in newCoordinates:
                    newCoordinates.remove(bodySegment)
        #return new bodyless coordinates
        return newCoordinates

    def weightLargeSnakes(self):
        """Negatively weight squares where larger snake heads could move to next round"""

        ourSnake = self.snakes[self.us]
        ourSize = ourSnake.getSize()
        for otherSnake in self.snakes:
            if otherSnake != self.us:
                otherSnakeSize = self.snakes[otherSnake].getSize()
                if  otherSnakeSize >= ourSize:
                    """Run this code for every snake on the board that's
                    not you AND longer or equal to you"""
                    headCoords = self.snakes[otherSnake].getHeadPosition()
                    x = headCoords[0]
                    y = headCoords[1]
                    """Weight coordinates left and right to 0, provided that
                    they are within the board indices (0 - width-1)"""
                    if x > 0:
                        if x < self.width-1:
                            self.board.setWeights([[x+1, y], [x-1, y]], 0)
                        else:
                            self.board.setWeights([[x-1, y]], 0)
                    else:
                        self.board.setWeights([[x+1, y]], 0)

                    """Weight coordinates up and down to 0, provided that
                    they are within the board indices (0 - height-1)"""
                    if y > 0:
                        if y < self.height-1:
                            self.board.setWeights([[x, y+1], [x, y-1]], 0)
                        else:
                            self.board.setWeights([[x, y-1]], 0)
                    else:
                        self.board.setWeights([[x, y+1]], 0)

    def weightSafeTails(self):
        """Weight locations that will be moved out of next turn as safe"""
        #TODO
        #For all snakes whose head is not adjacent to a food:
        #Weight the space occupied by their tail as 50 (or other positive value)

        for allSnakes in self.snakes:
            if allSnakes != self.us:
                #Run this code for ever snake that's not us
                otherSnakePos = self.snakes[allSnakes].getAllPositions()
                tailPos = otherSnakePos[-1]
                headPos = otherSnakePos[0]
                headX = headPos[0]
                headY = headPos[1]
                moveOptions = []
                foodOpt = False

                #Save possible moves that are within the board (including body)
                if (headX - 1) >= 0:
                    moveOptions.append([headX - 1, headY])
                if (headX + 1) < self.width:
                    moveOptions.append([headX + 1, headY])
                if (headY + 1) < self.height:
                    moveOptions.append([headX, headY + 1])
                if (headY - 1) >= 0:
                    moveOptions.append([headX, headY - 1])

                #If any possible move is to food, tail is not safe
                for coords in moveOptions:
                    if coords in self.food:
                        #Food is a possible movement
                        foodOpt = True
                        break

                if not foodOpt:
                    self.board.setWeight(tailPos, 50)

    def weightEnclosedSpaces(self, u):
        """Negatively weight enclosed spaces to prevent us from going in."""

        # print self.snakes[self.us].getAllPositions()[-1]
        # print u
        #self.board.showWeights(True, True)
        tailPos = self.snakes[self.us].getTailPosition()
        h = self.snakes[self.us].getAllPositions()[0]
        path = self.board.optimumPath(h, u) #Current goal
        self.board.setWeight(tailPos, 1)
        self.board.setEdges()
        if self.board.optimumPathLength(u, tailPos) != float('inf'):
            return path[1]
        us_id = self.us
        for snk in self.snakes: #Set weight of all possible next moves of other snakes to 0.
            if self.snakes[snk].getIdentifier() == us_id:
                ourSnake = self.snakes[snk]
                continue
            headPos = self.snakes[snk].getHeadPosition()
            headX = headPos[0]
            headY = headPos[1]
            n = []
            if (headX - 1) >= 0:
                n.append([headX-1, headY])
            if (headX + 1) < self.width:
                n.append([headX+1, headY])
            if (headY + 1) < self.height:
                n.append([headX, headY+1])
            if (headY - 1) >= 0:
                n.append([headX, headY-1])
            self.board.setWeights(n, 0)
            #self.board.showWeights(True,True)
        ourHead = ourSnake.getHeadPosition()
        path = self.board.optimumPath(ourHead, u) #Current goal
        otherOptions = []
        ourHeadX = ourHead[0]
        ourHeadY = ourHead[1]
        if (ourHeadX - 1) >= 0:
            otherOptions.append([ourHeadX-1, ourHeadY])
        if (ourHeadX + 1) < self.width:
            otherOptions.append([ourHeadX+1, ourHeadY])
        if (ourHeadY + 1) < self.height:
            otherOptions.append([ourHeadX, ourHeadY+1])
        if (ourHeadY - 1) >= 0:
            otherOptions.append([ourHeadX, ourHeadY-1])

        otherOptions.remove(path[1]) #Remove from other options our current option
        if len(ourSnake.getAllPositions()) > 1 and ourSnake.getAllPositions()[1] in otherOptions:
            # Remove our 'neck' from other otherOptions
            otherOptions.remove(ourSnake.getAllPositions()[1])
        for ot in otherOptions:
            if self.board.getWeight(ot) == 0:
                otherOptions.remove(ot)
        dont = False
        for other_opt in otherOptions:
            if self.board.optimumPathLength(other_opt, u) == float('inf'):
                dont = True
        self.board.setWeights(n, 1)
        if dont:
            return otherOptions[0]
        return path[1]
        #TODO
        #set other snake options to 1
        # Do not kill ourselves by picking a corner where we trap ourselves
        # How long are we?
        # Are we giving other people the opportunity to block off our exit?
        # What is the optimal traversal path to maximize future space opportunities
        # Don't limit our moves (against a surface) unless advantageous or necessary

    def weightTrapSnakes(self):
        """Positively weight squares that will allow us to block other snakes off"""
        #TODO
        #How long are they?
        #How much traversal room are we leaving them?
        #Do they need food? Do they have it in the trapped location?
        #How long are we? Can we effectively block them for long enough?

    def showBoard(self):
        """Use to show board with weight and colours """
        self.board.showWeights(True, True)
    def getFarthestLocationTrapped(self, pos):
        availableToUs = []
        availableToUs = self.set.getConnectedToWall(pos)
        print("This is the available nodes to us : ",availableToUs)
        farthestLocation = []
        farthestDistance = 0
        for x in availableToUs:
            xc = availableToUs[x][0]
            yc = availableToUs[x][1]
            distance = (abs(yc - pos[1])/abs(xc - pos[0]))
            print("THIS IS THE FUCKING DISTANCE ",distance)
            print()
            if distance > farthestDistance:
                farthestLocation = x
                farthestDistance = distance
        return farthestLocation
    def getLongestPath(self,u,v):
        pass
        return 0
    
    def extendPath(self, u, v):
        """
        Used in TRAPPED State. Extends the path between two points to a longer path. Usually u and v are adjacent.
        param1: [int,int] - x,y coords of a node.
        param2: [int,int]] - x,y coords of a node.

        return: path - path between u and v.
        """
        surrounding = []
        surrounding = self.set.getSurrounding(u)
        if len(surrounding != 0):
            path = self.board.optimumPath(surrounding[0],v)
            return path
        else:
            path = self.board.optimumPath(u,v)
            return path