"""Food tracking object for use in Game."""

class Food:
    """
    Tracks all food in the game.

    Has the following attributes:
    positions       [[x,y]]  - list of food positions
    """

    def __init__(self, foodList):
        """
        Initialize the Food class.

        param1: [[x, y]] - list of all food on the board
        """
        if 'data' in foodList:
            self.positions = foodList['data']
        else:
            self.positions = [[]]

    def update(self, foodList):
        """
        Overwrite the list of food positions.

        param1: [[x, y]] - list of all food on the board
        """
        self.positions = foodList['data']

    def getPositions(self):
        """
        Return food positions
        return: [[x, y]] - food positions
        """
        return self.positions
