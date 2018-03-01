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
            'object': 'world',
            'game_id': 'gameid',
        	'you': {},
            'snakes': {
                'object': 'list',
                'data': []
            },
        	'height': height,
        	'width': width,
            'turn': 0,
        	'food': {
                'object': 'list',
                'data': []
            },
        }

        self.extend = {} #stores snakes that have just eaten food

        for name in snakes:
            self.state['snakes']['data'].append({ 
                'taunt': 'gotta go!', 
                'name': name, 
                'id': name, 
                'length': 1,
                'health': 100,
                'object': 'snake',
                'body': {
                    'object': 'list',
                    'data': []
                }
            })
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
            possPoint = {
                'object': 'point',
                'x': possibleLoc[0],
                'y': possibleLoc[1]
            }
            self.state['snakes']['data'][i]['body']['data'].append(possPoint)
            occupied.append(possibleLoc)

        self.state['food']['data'] = [] #declare here so that below function call works
        self.placeFood(numFood)


    def move(self, snakeName, move):
        for snake in self.state['snakes']['data']:
            if snake['name'] != snakeName: continue

            # the below expressions add the next head position to the front of the coords list
            # the list comprehensions apply the [*,*] transformation to the current head
            currentHead = snake['body']['data'][0]
            if move == 'up':
                currentHead['y'] -= 1
                snake['body']['data'].insert(0, currentHead)
            elif move == 'right':
                currentHead['x'] += 1
                snake['body']['data'].insert(0, currentHead)
            elif move == 'down':
                currentHead['y'] += 1
                snake['body']['data'].insert(0, currentHead)
            elif move == 'left':
                currentHead['x'] -= 1
                snake['body']['data'].insert(0, currentHead)

            # the 'extend' variable is used as per the battlesnake spec when we move
            # forward next, our tail stays in place
            if self.extend[snakeName] == 0:
                snake['body']['data'] = snake['body']['data'][:-1] # remove tail if no extension
            else:
                self.extend[snakeName] -= 1

            if snake['body']['data'][0] in self.state['food']['data']: # food actually removed in updateState()
                self.extend[snakeName] += 1
                snake['length'] += 1


    def getPersonalizedState(self, name): # show 'you' for correct snake
        self.state['you'] = list(filter(lambda mySnake: mySnake['name'] == name, self.state['snakes']['data']))[0]
        return json.dumps(self.state)


    def updateState(self):
        toBeKilled = set() # this is a set to avoid duplicates from multiple iterations (may not be necessary)
        
        for snake in self.state['snakes']['data']:

            headPos = snake['body']['data'][0]
            if headPos in self.state['food']['data']: # if snake eats food
                self.state['food']['data'].remove(headPos)
                snake['health'] = 100

            snake['health'] -= 1 # decrement health and check if dead
            if(snake['health'] == 0):
                print('ran out of food')
                toBeKilled.add(snake['name'])
                continue

            if(headPos['x'] < 0 or headPos['x'] > (self.width - 1) or headPos['y'] < 0 or headPos['y'] > (self.height - 1)):
                print('wall hit')
                toBeKilled.add(snake['name'])
                continue

            for collider in self.state['snakes']['data']: # check our snake position against others

                colliderCoords = collider['body']['data']

                if headPos in colliderCoords[1:]:
                    if snake == collider:
                        print('collided with self')
                    else:
                        print('collided with snake body')
                    toBeKilled.add(snake['name'])
                    continue
                    
                colliderHead = colliderCoords[0] # hit head and this snake is smaller
                if snake != collider and headPos['x'] == colliderHead['x'] and headPos['y'] == colliderHead['y']:
                    if snake['length'] + self.extend[snake['name']] < collider['length'] + self.extend[collider['name']]:
                        print('collided with larger snake head')
                        toBeKilled.add(snake['name'])

        for snake in toBeKilled: # kill snakes here as to avoid changing looping dict
            current = [x for x in self.state['snakes']['data'] if x['name'] == snake][0]
            self.state['snakes']['data'].remove(current)

        self.checkFood()
        self.state['turn'] += 1

        return list(toBeKilled) # return to allow main.py to stop sending move requests


    def checkFood(self): # ensure propper amount of food
        current = len(self.state['food']['data'])
        desired = self.numFood

        if current < desired:
            self.placeFood(desired - current)


    def placeFood(self, numFood): # randomly place food in an available spot
        occupied = self.getOccupied() 
        for _ in range(0, numFood):
            valid = False
            possibleLoc = None
            while not valid:
                valid = True
                possibleLoc = [randint(0, self.width - 1), randint(0, self.height - 1)] # pick a random spot
                if possibleLoc in occupied:
                    valid = False

            possPoint = {
                'object': 'point',
                'x': possibleLoc[0],
                'y': possibleLoc[1]
            }
            self.state['food']['data'].append(possPoint) # we have found a free spot
            occupied.append(possibleLoc)


    def getOccupied(self): # list of squares that have stuff in
        occupied = []
        for snake in self.state['snakes']['data']:
            pointCoords = list(map(lambda point: [point['x'], point['y']], snake['body']['data']))
            occupied += pointCoords
        occupied += list(map(lambda point: [point['x'], point['y']], self.state['food']['data']))
        return occupied