"""Server to rapidly simulate games to determine loss trends"""

from random import randint

if __name__ == '__main__':
    print("We're up!")

    state = {
    	"you": "you",
    	"turn": 1,
    	"snakes": [
    		{
    			"taunt": "gotta go fast",
    			"name": "sneakysnake",
    			"id": "you",
    			"health_points": 100,
    			"coords": [
    				[
    					11,
    					5
    				],
    				[
    					11,
    					6
    				],
    				[
    					11,
    					7
    				]
    			]
    		}
    	],
    	"height": 20,
    	"width": 20,
    	"game_id": "gameid",
    	"food": [
    		[
    			5,
                4
    		]
    	],
    	"dead_snakes": []
    }

def initSnake():
    valid = false
    while(not valid):
        location = (randint(0,19), randint(0,19))

def printGames(games, p, m):
    #given games[], print to file/directory p
    #if m(bool), print each game to a different file
    return

def stepSnakes(gameState):
    #send gameState to each snake and waits for a response
    return

def incrementState(snake, move):
    #increments snake position in game state using move
    return

def generateFood(numItems):
    #check to see if a random food item is due to be added
    return

## Accept command inputs ##
#-s 'game state to run from'
#   if not present, use default
#-n 'number of games to run'
#   will have hard upper limit
#-p 'path for game outcomes'
#   if not present, use default
#-m 'print separate files for each game'
#   if not present, all games in one file
#-f 'number of food items at any one time'
#   if not present, use default

## Generate game state to send to snakes ##
## Given a move, modify the game state to match ##
## Build in local snakes and web snakes ##
