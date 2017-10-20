from random import randint

class State:
    def __init__(self, width, height, numSnakes, numFood):
        """
        Initialize the State class.

        param1: integer - width of board
        param2: integer - height of board
        param3: integer - number of snakes to create
        """

        if(numSnakes + numFood) > (width * height):
            raise ValueError('Not enough space on board')

        self.width = width  # declare size of board
        self.height = height

        self.state = {
        	"you": "you",
        	"turn": 1,
        	"snakes": [
        		{
        			"taunt": "gotta go fast",
        			"name": "sneakysnake",
        			"id": "you",
        			"health_points": 100,
        			"coords": []
        		}
        	],
        	"height": 20,
        	"width": 20,
        	"game_id": "gameid",
        	"food": [],
        	"dead_snakes": []
        }

        for i in range(1, numSnakes):
            self.state["snakes"].append({ "taunt": "gotta go slow", "name": "snake" + str(i - 1), "id": str(i - 1), "health_points": 100, "coords": [] })

        occupied = []
        for i in range(0, numSnakes):
            valid = False
            possibleLoc = None
            while not valid:
                valid = True
                possibleLoc = (randint(0, width - 1), randint(0, height - 1))
                for occupiedLoc in occupied:
                    if possibleLoc[0] == occupiedLoc[0] and possibleLoc[1] == occupiedLoc[1]:
                        valid = False
            self.state["snakes"][i]["coords"].append(possibleLoc)
            occupied.append(possibleLoc)

        for i in range(0, numSnakes):
            valid = False
            possibleLoc = None
            while not valid:
                valid = True
                possibleLoc = (randint(0, width - 1), randint(0, height - 1))
                for occupiedLoc in occupied:
                    if possibleLoc[0] == occupiedLoc[0] and possibleLoc[1] == occupiedLoc[1]:
                        valid = False
            self.state["snakes"][i]["coords"].append(possibleLoc)
            occupied.append(possibleLoc)



    def update(self, snake, move):
        return True

    def getState(self):
        return self.state
