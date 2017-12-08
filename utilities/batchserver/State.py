import json
from random import randint

class State:
    def __init__(self, width, height, snakes, numFood):
        """
        Initialize the State class.

        param1: integer - width of board
        param2: integer - height of board
        param3: integer - number of snakes to create
        """
        numSnakes = len(snakes)
        if numSnakes < 1:
            raise ValueError('Need have at least one snake')
        if(numSnakes + numFood) > (width * height):
            raise ValueError('Not enough space on board')

        self.width = width  # declare size of board
        self.height = height

        self.state = {
        	"you": "",
        	"turn": 1,
        	"snakes": [],
        	"height": 20,
        	"width": 20,
        	"game_id": "gameid",
        	"food": [],
        	"dead_snakes": []
        }

        for name in snakes:
            self.state["snakes"].append({ "taunt": "gotta go!", "name": name, "id": name, "health_points": 100, "coords": [] })

        occupied = []
        for i in range(0, numSnakes): #place randomly on board
            valid = False
            possibleLoc = None
            while not valid:
                valid = True
                possibleLoc = [randint(0, width - 1), randint(0, height - 1)]
                for occupiedLoc in occupied:
                    if possibleLoc[0] == occupiedLoc[0] and possibleLoc[1] == occupiedLoc[1]:
                        valid = False
            self.state["snakes"][i]["coords"].append(possibleLoc)
            occupied.append(possibleLoc)

        for i in range(0, numFood):
            valid = False
            possibleLoc = None
            while not valid:
                valid = True
                possibleLoc = [randint(0, width - 1), randint(0, height - 1)]
                for occupiedLoc in occupied:
                    if possibleLoc[0] == occupiedLoc[0] and possibleLoc[1] == occupiedLoc[1]:
                        valid = False
            self.state["food"].append(possibleLoc)
            occupied.append(possibleLoc)


    def move(self, snakeName, move):
        #TODO: check for food infront, extend tail, create new head, potentially remove old tail
        print(snakeName)
        print(move)
        if move == 'up':
            self.state["snakes"]
        elif move == 'right':

        elif move == 'down':

        elif move == 'left':


    def setPos(self, snakeNum, coords):
        self.state["snakes"][snakeNum]["coords"] = coords


    def getState(self, name):
        self.state["you"] = name
        return json.dumps(self.state)


    def kill(self):
        #TODO: check for other snake collisions

        toBeKilled = []
        for snake in self.state["snakes"]:
            headPos = snake["coords"][0]
            if(headPos[0] < 0 or headPos[0] > (self.width - 1) or headPos[1] < 0 or headPos[1] > (self.height - 1)):
                toBeKilled.append(snake)

        for snake in toBeKilled:
            self.state["dead_snakes"].append(snake)
            self.state["snakes"].remove(snake)