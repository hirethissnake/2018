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

        self.extend = {} #stores snakes that have just eaten food

        for name in snakes:
            self.state["snakes"].append({ "taunt": "gotta go!", "name": name, "id": name, "health_points": 100, "coords": [] })
            self.extend[name] = 0

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

        self.state["food"] = [] #declar here so that below function call works
        self.placeFood(numFood)


    def move(self, snakeName, move):
        for snake in self.state["snakes"]:
            if snake["name"] != snakeName: continue

            currentHead = snake["coords"][0]
            if move == 'up':
                snake["coords"].insert(0, [sum(x) for x in zip(currentHead, [0,-1])])
            elif move == 'right':
                snake["coords"].insert(0, [sum(x) for x in zip(currentHead, [1,0])])
            elif move == 'down':
                snake["coords"].insert(0, [sum(x) for x in zip(currentHead, [0,1])])
            elif move == 'left':
                snake["coords"].insert(0, [sum(x) for x in zip(currentHead, [-1,0])])

            if self.extend[snakeName] == 0:
                snake["coords"] = snake["coords"][:-1]
            else:
                self.extend[snakeName] -= 1

            if snake["coords"][0] in self.state["food"]: #note: food removed in kill() function
                self.extend[snakeName] += 1


    def setPos(self, snakeNum, coords): #just used for testing/debugging
        self.state["snakes"][snakeNum]["coords"] = coords


    def getState(self, name):
        self.state["you"] = name
        return json.dumps(self.state)


    def kill(self):
        #TODO: check for other snake collisions - check extend{} length in addition to regular length

        toBeKilled = []
        for snake in self.state["snakes"]:
            headPos = snake["coords"][0]
            if headPos in self.state["food"]:
                self.state["food"].remove(headPos)
            if(headPos[0] < 0 or headPos[0] > (self.width - 1) or headPos[1] < 0 or headPos[1] > (self.height - 1)):
                toBeKilled.append(snake)

        for snake in toBeKilled:
            self.state["dead_snakes"].append(snake)
            self.state["snakes"].remove(snake)

    def checkFood(self):
        if len(self.state["food"]) == 0:
            self.placeFood(1)

    def placeFood(self, numFood):
        occupied = self.getOccupied()
        for i in range(0, numFood):
            valid = False
            possibleLoc = None
            while not valid:
                valid = True
                possibleLoc = [randint(0, self.width - 1), randint(0, self.height - 1)]
                for occupiedLoc in occupied:
                    if possibleLoc[0] == occupiedLoc[0] and possibleLoc[1] == occupiedLoc[1]:
                        valid = False
            self.state["food"].append(possibleLoc)
            occupied.append(possibleLoc)

    def getOccupied(self):
        occupied = []
        for snake in self.state["snakes"]:
            occupied += snake["coords"]
        occupied += self.state["food"]
        return occupied