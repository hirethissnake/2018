"""Server to rapidly simulate games to determine loss trends"""

import sys
import json
import time
import requests
from State import State


def runGame(snakesFile):
    snakeUrls = []
    with open(snakesFile) as f:
        snakeUrls = f.read().split("\n")

    snakes = {}
    for url in snakeUrls:
        response = requests.post(url + "/start", data=json.dumps({"width": 20, "height": 20, "game_id": "gameid"}), headers={'content-type': 'application/json'})
        snakes[eval(response.text)["name"]] = url + "/move"    

    state = State(20, 20, list(snakes.keys()), 4)
    
    while(len(snakes) != 0):

        for name in snakes:
            print(state.state)
            response = requests.post(snakes[name], data=state.getState(name), headers={'content-type': 'application/json'})
            move = eval(response.text)["move"]
            print(move)
            state.move(name, move)
        
        state.kill()

        #TODO: update snakes dictionary to remove dead snakes
        print(state.state)
        print()

        time.sleep(2)


def printGames(games, p, m):
    #given games[], print to file/directory p
    #if m(bool), print each game to a different file
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

if __name__ == '__main__':
    if len(sys.argv) != 3 or not sys.argv[1].isdigit():
        raise ValueError('Invalid arguments')
    for i in range(0, int(sys.argv[1])):
        runGame(sys.argv[2])
