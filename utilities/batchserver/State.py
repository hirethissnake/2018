import json
from random import randint

class State:

    def __init__(self, width, height, snakes, numFood):
        numSnakes = len(snakes)
        if numSnakes < 1:
            raise ValueError('Need have at least one snake')
        if(numSnakes + numFood) > (width * height):
            raise ValueError('Not enough space on board')

        self.width = width  # declare size of board
        self.height = height
        self.numFood = numFood

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

        self.state["food"] = [] #declare here so that below function call works
        self.placeFood(numFood)


    def move(self, snakeName, move):
        for snake in self.state["snakes"]:
            if snake["name"] != snakeName: continue

            # add new coord to front of list
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


    def updateState(self):
        toBeKilled = set()
        for snake in self.state["snakes"]:

            headPos = snake["coords"][0]
            if headPos in self.state["food"]: # snake eats food
                self.state["food"].remove(headPos)
                snake["health_points"] = 100

            snake["health_points"] -= 1 # decrement health and check if dead
            if(snake["health_points"] == 0):
                print("ran out of food")
                toBeKilled.add(snake["name"])
                continue

            if(headPos[0] < 0 or headPos[0] > (self.width - 1) or headPos[1] < 0 or headPos[1] > (self.height - 1)):
                print("wall hit")
                toBeKilled.add(snake["name"])
                continue

            for collider in self.state["snakes"]: # check our snake position against others

                colliderCoords = collider["coords"]

                if headPos in colliderCoords[1:]: # hit body
                    print("collider coords")
                    print(collider["coords"])
                    print(collider["coords"][1:])
                    toBeKilled.add(snake["name"])
                    continue
                    
                colliderHead = colliderCoords[0] # hit head and this snake is smaller
                if snake != collider and headPos[0] == colliderHead[0] and headPos[1] == colliderHead[1]:
                    if len(snake["coords"]) + self.extend[snake["name"]] < len(collider["coords"]) + self.extend[collider["name"]]:
                        print("collider extend:")
                        print(len(snake["coords"]) + self.extend[snake["name"]])
                        print(len(collider["coords"]) + self.extend[collider["name"]])
                        print(collider["coords"][0])
                        print(headPos)
                        toBeKilled.add(snake["name"])

        for snake in toBeKilled: # kill snakes here as looping through dict above
            current = [x for x in self.state["snakes"] if x["name"] == snake][0]
            self.state["dead_snakes"].append(current)
            self.state["snakes"].remove(current)

        self.checkFood()
        self.state["turn"] += 1

        return list(toBeKilled)


    def checkFood(self): # fix to match numFood from init
        current = len(self.state["food"])
        desired = self.numFood

        if current < desired:
            self.placeFood(desired - current)


    def placeFood(self, numFood):
        occupied = self.getOccupied()
        for _ in range(0, numFood):
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