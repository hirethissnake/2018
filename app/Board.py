"""
Calculate best path and path benefits.
Includes vertices and edges.
"""

import colorsys
import numpy as np
#import igraph
from scipy.sparse.csgraph import dijkstra
try:
    from appJar import gui
except ImportError:
    print('Failed to import appJar')


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


    def checkNode(self, x, y):
        """
        Check if u is a valid node.

        param1: [int, int] - node in the form [x, y]
        """

        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError('indices should be integers')
        if x >= self.width or x < 0 or y >= self.height or y < 0:
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

        return: [integer] - array with [width, height]
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
        return 100 - weight


    def setWeight(self, x, y, weight):
        """
        Set incoming edges of vertex u to weight.

        param1: [int, int] - node in the form [x, y]
        param2: integer/float - weight to set
        """

        self.modifyWeightErrorCheck(x, y, weight)  # comment this out for speed
        weight = self.normalizeWeight(weight)

        self.board[x, y] = weight


    def resetWeights(self):
        """
        Reset all weights to 50.
        """

        self.board = np.full((self.width, self.height), 50, dtype='f')


    def setWeights(self, nodes, weight):
        """
        Modify a list of node weights.

        param1: [[int, int]] - array of nodes in the form [<integer>,<integer>]
        param2: float/int - weight to set
        """

        cols, rows = map(list, zip(*nodes)) # create a lists of columns and rows to be modified

        weight = self.normalizeWeight(weight)

        for i in range(len(nodes)):
            self.modifyWeightErrorCheck(cols[i], rows[i], weight)  # comment this out for speed

        self.board[cols, rows] = weight


    def modifyWeights(self, operator, nodes, value):
        """
        Modify a list of node weights.

        param1: string - operator ('*', '/', '+', '-')
        param2: [[int, int]] - array of nodes in the form <integer>,<integer>
        param3: float/int - value to modify by
        """

        self.modifyWeightsErrorCheck(operator)  # comment these out for speed
        self.checkNumber(value)

        for node in nodes:
            self.checkNode(*node)  # comment this out for speed
            if operator == "*":
                self.multiplyWeight(*node, value)
            elif operator == "/":
                self.divideWeight(*node, value)
            elif operator == "+":
                self.addWeight(*node, value)
            elif operator == "-":
                self.subtractWeight(*node, value)


    @staticmethod
    def modifyWeightsErrorCheck(operator):
        """
        Check modifyWeights() method for errors.

        param1: string - operator to check
        """

        if operator != '*' and operator != '/' and operator != '+' \
                    and operator != '-':
            raise ValueError('invalid operator')


    def multiplyWeight(self, x, y, multiplier):
        """
        Multiply weight of node u by multiplier.

        param1: [int, int] - node in the form [x, y]
        param2: integer/float - number to multiply weight by
        """

        self.modifyWeightErrorCheck(x, y, multiplier)  # comment this out for speed

        self.setWeight(x, y, (self.getWeight(x, y) * multiplier))


    def divideWeight(self, x, y, divisor):
        """
        Divide weight of node u by divisor.

        param1: [int, int] - node in the form [x, y]
        param2: integer/float - number to divide weight by
        """

        self.modifyWeightErrorCheck(x, y, divisor)  # comment this out for speed

        self.setWeight(x, y, self.getWeight(x, y) // divisor)


    def addWeight(self, x, y, addend):
        """
        Increase weight of node u by addend.

        param1: [int, int] - node in the form [x, y]
        param2: integer/float - number to add to weight
        """

        self.modifyWeightErrorCheck(x, y, addend)  # comment this out for speed

        currentWeight = self.getWeight(x, y)
        self.setWeight(x, y, currentWeight + addend)


    def subtractWeight(self, x, y, subtrahend):
        """
        Decrease weight of node u by subtrahend.

        param1: [int, int] - node in the form [x, y]
        param2: integer/float - number to subtract from weight
        """

        self.modifyWeightErrorCheck(x, y, subtrahend)  # comment this out for speed

        currentWeight = self.getWeight(x, y)
        self.setWeight(x, y, currentWeight - subtrahend)


    def modifyWeightErrorCheck(self, x, y, num):
        """
        Check weight modification method for errors.

        param1: unknown - item to confirm if node
        param2: unknown - item to confirm if integer/float
        """

        self.checkNode(x, y)
        self.checkNumber(num)


    def getWeight(self, x, y):
        """
        Return the weight of the node u from the dictionary.

        param1: [int, int] - node in the form [x, y]
        return: integer/float - weight of node u
        """

        self.checkNode(x, y)  # comment this out for speed
        weight = self.board[x, y]
        returnable = 0
        if weight < 0:
            returnable = 0
        elif weight < 100:
            returnable = int(100 - weight)
        return returnable


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


    def isNodeWeightUnique(self, x, y):
        """
        Return False if weight appears more than once in the graph.

        param1: [int, int] - node in the form [x, y]
        return: boolean - True if weight is unique, Fale otherwise
        """
        if self.countNodeWeightCopies(x, y) > 1:
            return False
        return True


    def countNodeWeightCopies(self, x, y):
        """
        Returns the number of nodes with the same weight as the given node (minimum 1).

        param1: [int, int] - node in the form [x, y]
        return: int - Returns number of other nodes with same weight
        """

        self.checkNode(x, y)  # comment this out for speed

        targetWeight = 100 - self.getWeight(x, y)
        return np.count_nonzero(self.board == targetWeight)


    def optimumPath(self, vertices):
        """
        Return shortest path between nodes from u to v.

        u: [int, int] - start node in the form [x, y]
        v: [int, int] - end node in the form [x, y]
        return: [[int, int]] - node names in the optimum path from u to v
        """
        # pylint: disable=C0301
        # credit to https://stackoverflow.com/questions/16329403/how-can-you-make-an-adjacency-matrix-which-would-emulate-a-2d-grid
        # and http://codegists.com/snippet/python/dijkstra_examplepy_myjr52_python
        # for assisting in making this method happen

        # Check that we're given two vertices to pathfind between
        if len(vertices) != 2:
            raise ValueError("Can only find path between two vertices.")

        # Make some nice variables for working with
        b_height, b_width = self.board.shape
        u = vertices[0]
        v = vertices[1]
        start = u[1] * b_width + u[0]
        end = v[1] * b_width + v[0]

        # Create the adjacency matrix
        adj_matrix = np.zeros((b_height * b_width, b_height * b_width), dtype=self.board.dtype)
        for y in range(b_height):
            for x in range(b_width):
                # map x, y coords to a range from 0 to (b_height * b_width)
                i = y * b_width + x
                if x > 0:
                    adj_matrix[i - 1, i] = self.board[i // b_width][i % b_width]
                    adj_matrix[i, i - 1] = self.board[i // b_width][i % b_width]
                if y > 0:
                    adj_matrix[i - b_width, i] = self.board[i // b_width][i % b_width]
                    adj_matrix[i, i - b_width] = self.board[i // b_width][i % b_width]
        # Perform the Dikstra
        (distances, previous) = dijkstra(adj_matrix, indices=start,\
                                         directed=True, return_predecessors=True)

        # Collect the path between points using the previous array, but avoid if there are no paths
        path = []
        i = end
        if np.isinf(distances[i]):
            return None
        else:
            while i != start:
                path.append([i % b_width, i // b_width])
                i = previous[i]
            path.append([start % b_width, start // b_width])

        return path[::-1]


    def optimumPathErrorCheck(self, vertices):
        """
        Check optimumPath() method for errors.

        Mostly checks for duplicate vertices.

        vertices: list - items to confirm as nodes ([x, y])
        """
        if len(vertices) != len(set([(x, y) for x, y in vertices])):
            raise ValueError("There cannot be duplicate vertices in a path.")
        for vertex in vertices:
            self.checkNode(vertex[0], vertex[1])

        return True


    def optimumPathLength(self, vertices):
        """
        Return length of optimal path between two vertices.

        vertices: [start, finish] - from start to finish, both as [int, int]
        return: int - length of path
        """
        return len(self.optimumPath(vertices))


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


    def showPath(self, vertices):
        """
        Visualize optimal path between two vertices.

        vertices: [start, finish] - from start to finish, both as [int, int]
        """

        self.optimumPathErrorCheck(vertices)  # comment this out for speed

        self.showCombiner(self.optimumPath(vertices), True, True)


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
                weight = self.getWeight(col, row)

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
