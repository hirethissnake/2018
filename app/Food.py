"""Food tracking object for use in Game."""

class Food:
    """
    Tracks all food in the game.

    Has the following attributes:
    positions       ([coords])  - list of food positions
    """

    def __init__(self, positions):
        """
        Initialize the Food class.

        param1: [[x, y]] - list of all food on the board
        """
        self.positions = positions

    def update(self, positions):
        """
        Overwrite the list of food positions.

        param1: [[x, y]] - list of all food on the board
        """
        self.positions = positions

    def getPositions(self):
        """
        Return food positions
        return: [[x, y]] - food positions
        """
        return self.positions
