"""
Calculate best path and path benefits.
Includes vertices and edges.
"""

import colorsys
import numpy as np
#import igraph
from scipy.sparse.csgraph import dijkstra
#try:
#    from appJar import gui
#except ImportError:
#    print('Failed to import appJar')


class Board:
    """
    Store square weight and calculate optimal paths between them.

    Has the following public methods:

## OPERATORS ##     ## RETURN ##

__init__                void        Board initialization
averageWeights          void        Balance weight values using heat equation
modifyWeights           void        Operate on array of vertexes by array of
                                        weights (parent for next four functions)
multiplyWeight          void        Multiply weight of node by multiplier
divideWeight            void        Divide weight of node by divisor
addWeight               void        Increase weight of node by addend
subtractWeight          void        Decrease weight of node by subtrahend

## GETTERS ##

getNodeWithPriority     [x,y]       Return vertex name with priority of some value
getNodesWithPriority    [[x, y]]    Return array of vertexes with priority
                                        between start and end
getSize                 [int, int]  Get board size as an x, y array
getWeight               int/float   Return the weight of a node u
isNodeWeightUnique      boolean     Check if node weight exists in board twice
countNodeWeightCopies   int         Get the number of copies a specific weight
optimumPath             [[x, y]]    Get the best path between two nodes

## SETTERS ##

setWeight               void        Set incoming edges of vertex u to some
                                        weight
setWeights              void        Set incoming edges of array of vertexes to
                                        matching weight in array

## DISPLAY ##
showWeights             void        Opens visualization of weights of all nodes
showPath                void        Display graphic of best path between nodes
    """


    def __init__(self, width, height):
        """
        Initialize the Graph class.

        param1: integer - width of board
        param2: integer - height of board
        """

        self.initErrorCheck(width, height)  # comment this out for speed

        self.width = width  # declare size of board
        self.height = height

        self.board = np.full((width, height), 50, dtype='f')

        self.adjMatrixOutOfDate = True
        self.adjMatrix = None


    def initErrorCheck(self, width, height):
        """
        Check init() for errors.

        param1: integer - width to check
        param2: integer - height to check
        """

        self.checkInt(width)
        self.checkInt(height)

        if width <= 1:
            raise ValueError('width must be greater than 1')
        if height <= 1:
            raise ValueError('height must be greater than 1')


    def checkNode(self, u):
        """
        Check if there is a node u.

        param1: [int, int] - node in the form [x, y]
        """

        if u[0] >= self.width or u[0] < 0 or u[1] >= self.height or u[1] < 0:
            raise ValueError('node is out of bounds')


    @staticmethod
    def checkNumber(num):
        """
        Check if num is an integer/float.

        param1: unknown - item to confirm if integer/float
        """

        if not isinstance(num, int) and not isinstance(num, float):
            raise ValueError('number must be an integer/float')


    @staticmethod
    def checkInt(num):
        """
        Check if num is an integer.

        param1: unknown - item to confirm if integer
        """

        if not isinstance(num, int):
            raise ValueError('number must be an integer')


    def getSize(self):
        """
        Return board size.

        return: [int, int] - board size as [width, height]
        """

        return list(self.board.shape)


    @staticmethod
    def normalizeWeight(weight):
        """
        Fit weight within expected parameters (0, 100).
        Internally, weight is 100 - given weight.
        """

        # reversed so that "really want to go to" looks like 100 to developer.
        # However, djikstra's minimizes distances so lower is better.
        if weight > 100:
            return 0
        elif weight <= 0:
            return np.inf
        return int(100 - weight)


    def setWeight(self, u, weight):
        """
        Set willingness of going to node to given weight.

        param1: [int, int] - node as [x, y]
        param2: integer/float - weight to set
        """

        self.modifyWeightErrorCheck(u, weight)  # comment this out for speed
        weight = self.normalizeWeight(weight)

        self.board[u[0], u[1]] = weight


    def resetWeights(self):
        """
        Reset all weights to 50.
        """

        self.board = np.full((self.width, self.height), 50, dtype='f')
        self.adjMatrixOutOfDate = True


    def setWeights(self, nodes, weight):
        """
        Modify a list of node weights.

        param1: [[int, int]] - array of nodes in the form [<integer>, <integer>]
        param2: float/int - weight to set
        """

        cols, rows = map(list, zip(*nodes)) # create a lists of columns and rows to be modified

        weight = self.normalizeWeight(weight)

        for i in range(len(nodes)):
            self.modifyWeightErrorCheck([cols[i], rows[i]], weight)  # comment this out for speed

        self.board[cols, rows] = weight
        self.adjMatrixOutOfDate = True


    def modifyWeights(self, operator, nodes, value):
        """
        Modify a list of node weights.

        param1: string - operator ('*', '/', '+', '-')
        param2: [[int, int], ] - array of nodes, each as [int, int]
        param3: float/int - value to modify by
        """

        self.modifyWeightsErrorCheck(operator)  # comment these out for speed
        self.checkNumber(value)

        for node in nodes:
            self.checkNode(node)  # comment this out for speed
            if operator == '*':
                self.multiplyWeight(node, value)
            elif operator == '/':
                self.divideWeight(node, value)
            elif operator == '+':
                self.addWeight(node, value)
            elif operator == '-':
                self.subtractWeight(node, value)


    @staticmethod
    def modifyWeightsErrorCheck(operator):
        """
        Check modifyWeights() method for errors.

        param1: string - operator to check
        """

        if operator != '*' and operator != '/' and operator != '+' \
                    and operator != '-':
            raise ValueError('invalid operator')


    def multiplyWeight(self, u, multiplier):
        """
        Multiply weight of node by multiplier.

        param1: [int, int] - node as [x, y]
        param2: integer/float - number to multiply weight by
        """

        self.modifyWeightErrorCheck(u, multiplier)  # comment this out for speed

        self.setWeight(u, self.getWeight(u) * multiplier)


    def divideWeight(self, u, divisor):
        """
        Divide weight of node by divisor.

        param1: [int, int] - node as [x, y]
        param2: integer/float - number to divide weight by
        """

        self.modifyWeightErrorCheck(u, divisor)  # comment this out for speed

        self.setWeight(u, self.getWeight(u) // divisor)


    def addWeight(self, u, addend):
        """
        Increase weight of node by addend.

        param1: [int, int] - node as [x, y]
        param2: integer/float - number to add to weight
        """

        self.modifyWeightErrorCheck(u, addend)  # comment this out for speed

        self.setWeight(u, self.getWeight(u) + addend)


    def subtractWeight(self, u, subtrahend):
        """
        Decrease weight of node by subtrahend.

        param1: [int, int] - node as [x, y]
        param2: integer/float - number to subtract from weight
        """

        self.modifyWeightErrorCheck(u, subtrahend)  # comment this out for speed

        self.setWeight(u, self.getWeight(u) - subtrahend)


    def modifyWeightErrorCheck(self, u, num):
        """
        Check weight modification method for errors.

        param1: unknown - item to confirm as node
        param2: unknown - item to confirm as integer/float
        """

        self.checkNode(u)
        self.checkNumber(num)


    def getWeight(self, u):
        """
        Return the weight of the node u.

        param1: [int, int] - node as [x, y]
        return: integer/float - weight of node u
        """

        self.checkNode(u) # comment this out for speed
        weight = self.board[u[0], u[1]]
        returnable = 0
        if weight < 0:
            returnable = 0
        elif weight < 100:
            returnable = 100 - weight
        return int(returnable)


    def getNodeWithPriority(self, offset):
        """
        Return vertex name with priority offset.

        param1: int - index to return priority (can be negative)
        return: [int, int] - node name with priority offset
        """

        self.checkInt(offset) # comment this out for speed

        # get index of nth largest value
        flatIndex = np.argpartition(self.board.flatten(), offset)[offset]
        # '//' operator forces integer division
        return [flatIndex // self.width, flatIndex % self.width]


    def getNodesWithPriority(self, start, end):
        """
        Return vertexes in order of highest (start) to lowest (end) priority.

        param1: int - start index to return priority
        param2: int - end index to return priority
        return: [[int, int]] - node names with priority from start-end
        """

        self.getNodesWithPriorityErrorCheck(start, end)  # comment for speed

        indices = []
        for i in range(end - start + 1):
            indices.append(self.getNodeWithPriority(start + i))
        return indices


    def getNodesWithPriorityErrorCheck(self, start, end):
        """
        Check getNodesWithPriority() for errors.

        param1: int - start index to return priority
        param2: int - end index to return priority
        """

        self.checkInt(start)
        self.checkInt(end)
        if start >= end:
            raise ValueError('start must be less than end')
        if start < 0 or end >= self.board.size:
            raise ValueError('value is out of bounds')


    def isNodeWeightUnique(self, u):
        """
        Return False if weight appears more than once in the graph.

        param1: [int, int] - node as [x, y]
        return: boolean - True if weight is unique, False otherwise
        """
        if self.countNodeWeightCopies(u) > 1:
            return False
        return True


    def countNodeWeightCopies(self, u):
        """
        Returns the number of nodes with the same weight as the given node (minimum 1).

        param1: [int, int] - node as [x, y]
        return: int - Returns number of other nodes with same weight
        """

        self.checkNode(u)  # comment this out for speed

        targetWeight = 100 - self.getWeight(u)
        # counts non-zero elements within board that satisfy the condition
        # element == targetWeight
        return np.count_nonzero(self.board == targetWeight)


    def optimumPath(self, u, v):
        """
        Return shortest path between nodes from u to v.

        u: [int, int] - start node in the form [x, y]
        v: [int, int] - end node in the form [x, y]
        return: [[int, int]] - node names in the optimum path from u to v
        """
        # credit to https://stackoverflow.com/questions/16329403/
        # and http://codegists.com/snippet/python/dijkstra_examplepy_myjr52_python
        # for assisting in making this method happen

        # Make some nice variables for working with
        bHeight, bWidth = self.board.shape
        adjMatrixSide = bHeight * bWidth
        start = u[1] * bWidth + u[0]
        end = v[1] * bWidth + v[0]

        # Update the adjacency matrix if it's out-of-date
        if self.adjMatrixOutOfDate:
            self.adjMatrixOutOfDate = False
            self.adjMatrix = np.zeros((adjMatrixSide, adjMatrixSide), dtype=self.board.dtype)

            for y in range(bHeight):
                for x in range(bWidth):
                    # map x, y coords to a range from 0 to (bHeight * bWidth)
                    i = y * bWidth + x
                    iWeight = self.board[i // bWidth][i % bWidth]
                    if x > 0:
                        self.adjMatrix[i - 1, i] = iWeight
                        self.adjMatrix[i, i - 1] = iWeight
                    if y > 0:
                        self.adjMatrix[i - bWidth, i] = iWeight
                        self.adjMatrix[i, i - bWidth] = iWeight

        # Perform the Djikstra
        (distances, previous) = dijkstra(self.adjMatrix, indices=start,\
                                         directed=True, return_predecessors=True)

        # Collect the path between points using the previous array, but avoid if there are no paths
        path = []
        i = end
        if np.isinf(distances[i]):
            return None
        else:
            while i != start:
                path.append([i % bWidth, i // bWidth])
                i = previous[i]
            path.append([start % bWidth, start // bWidth])

        return path[::-1]


    def optimumPathLength(self, u, v):
        """
        Return length of optimal path between two vertices.

        param1: [int, int] - start node as [x, y]
        param2: [int, int] - end node
        return: int - length of path
        """
        path = self.optimumPath(u, v)
        if path == None:
            return -1
        return len(self.optimumPath(u, v))


    def showWeights(self, colours, numbers):
        """
        Visualize weights of each node.

        param1: boolean - show colours on display?
        param2: boolean - show numbers on display?
        """

        self.showWeightsErrorCheck(colours, numbers)  # comment for speed

        self.showCombiner([], colours, numbers)


    @staticmethod
    def showWeightsErrorCheck(colours, numbers):
        """
        Check showWeights() method for errors.

        param1,2: unknown - item to check if boolean
        """

        if not isinstance(colours, bool):
            raise ValueError('colours must be a boolean')

        if not isinstance(numbers, bool):
            raise ValueError('numbers must be a boolean')


    def showPath(self, u, v):
        """
        Visualize optimal path between two vertices.

        param1: [int, int] - start node as [x, y]
        param2: [int, int] - end node
        """

        self.showCombiner(self.optimumPath(u, v), True, True)


    def showCombiner(self, pathValues, colours, numbers):
        """
        Visualize weights of each node.

        param1: array - path nodes to colour
        param1: boolean - show colours on display?
        param2: boolean - show numbers on display?
        """

        app = gui('Login Window', '950x950')
        app.setBg('white')
        app.setTitle('SneakySnake Visualiser')

        for row in range(self.height):
            for col in range(self.width):

                nodeName = str(row) + ',' + str(col)
                weight = self.getWeight([col, row])

                # interpolate square value from gridValue into HSV value
                # between red and green, convert to RGB, convert to hex
                hexCode = '#%02x%02x%02x' % tuple(i * 255 for i in
                            colorsys.hls_to_rgb((weight * 1.2) /
                            float(360), 0.6, 0.8))
                if weight == 0: # color perfect non-valid entries black
                    hexCode = '#000000'
                if weight == 100: # color perfect full-valid entries blue
                    hexCode = '#0033cc'
                if weight > 100 or (weight != float('-inf') and weight < 0):
                    # color invalid entries grey
                    hexCode = '#616161'
                if [row, col] in pathValues:
                    # color path values cyan
                    hexCode = '#66ffff'

                if numbers: # add numbers
                    app.addLabel(nodeName, '%.2f' % weight, col, row)
                else:
                    app.addLabel(nodeName, '', col, row)

                if colours is True: # add colours
                    app.setLabelBg(nodeName, hexCode)

        app.go() # show window
