"""Independent snake object for use in Game."""

class Snake:
    """
    Feisty snake object.

    Has the following attributes:
    size            int             - describes length of snake
    identifier      uuid            - unique identifier describing for each snake
    coords          [[x,y]]         - array of [x,y] describing snakes body
    healthPoints    int             - 0..100, describes moves a snake has before
                                        death, unless that snake eats food.
    oldHealthPoints int             - health_points of snake on last move
    oldCoords       [[x,y]]         - array of array of [x,y] describing past
                                        locations the snake was at
    taunt           string          - snake's current taunt
    name            string          - name of snake
    """

    def __init__(self, data):
        """
        Initialize the Snake class.

        param1: data - all snake-related data from server

        Raises: ValueError
            if: size not int.
        """

        # often updated
        self.identifier = data['id']
        self.coords = data['body']['data']
        self.healthPoints = data['health']
        self.size = data['length']
        # old
        self.oldSize = data['length']
        self.oldHealthPoints = data['health']
        self.oldCoords = [data['body']['data']]
        # snake personality
        if 'taunt' in data:
            self.taunt = data['taunt']
        if 'name' in data:
            self.name = data['name']

    def update(self, data):
        """
        Update snake after previous move.
        param1: data - all snake-related data from server

        """

        healthPoints = data['health']
        if healthPoints > 100 or healthPoints < 0:
            raise ValueError('health_points must be between 100 and 0')
        self.oldHealthPoints = self.healthPoints
        self.healthPoints = healthPoints

        self.oldSize = self.size
        self.size = data['length']

        self.coords = data['body']['data']

        if 'taunt' in data:
            self.taunt = data['taunt']

        self.oldCoords.insert(0, self.coords)

    def getSize(self):
        """
        Return snake size
        return: int - snake
        """

        return self.size

    def getHealth(self):
        """
        Return snake healthPoints
        return: int - healthPoints
        """

        return self.healthPoints

    def getHunger(self):
        """
        Return hunger of snake

        return: int - 100-healthPoints.
        """

        return 100 - self.healthPoints

    def getHeadPosition(self):
        """
        Return head position.
        return: array - as [x, y] coords.
        """

        return self.coords[0]

    def getAllPositions(self):
        """
        Return array of coords.

        return: array[array] - [x,y] of all body coords.
        """

        return self.coords

    def getTailPosition(self):
        """
        Return array of tail position.

        return: array - [x, y] of tail coords
        """

        return self.coords[-1]

    def getIdentifier(self):
        """
        Return snake's identifier.

        return: uuid (as string)
        """

        return self.identifier

    def toString(self):
        """
        Return Snake attribues as a string.
        """

        asString = 'identifer: ' + str(self.identifier) + '\n' \
                    + 'healthPoints: ' + str(self.healthPoints) + '\n' \
                    + 'coords: ' + str(self.coords)

        return asString

    @staticmethod
    def isInt(num, name):
        """Double check value is int."""
        if not isinstance(num, int):
            raise ValueError(str(name) + ' must be an integer')

    @staticmethod
    def isString(value, name):
        """Double check value is int."""
        if not isinstance(value, str):
            raise ValueError(str(name) + ' must be a string')
