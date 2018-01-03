"""Server to rapidly simulate games to determine loss trends"""

import sys
import json
import time
import requests
from State import State


def runGame(snakesFile):
    #TODO: add health system
    # add snake collisions
    # print games to a file when done
    # make sure game actually stops
    # add robusteness and proper command system
    # randomly spawn food
    # update taunts

    snakeUrls = []
    with open(snakesFile) as f:
        snakeUrls = f.read().split("\n")

    snakes = {}
    differentiationCounter = 0
    for url in snakeUrls:
        response = requests.post(url + "/start", data=json.dumps({"width": 20, "height": 20, "game_id": "gameid"}), headers={'content-type': 'application/json'})
        name = eval(response.text)["name"]
        while name in snakes:
            name = eval(response.text)["name"] + str(differentiationCounter)
            differentiationCounter += 1
        snakes[name] = url + "/move"    

    state = State(20, 20, list(snakes.keys()), 4)

    data = []
    while(len(snakes) != 0):
        data.append(json.dumps(state.state))
        toUpdate = []
        for name in snakes:
            response = requests.post(snakes[name], data=state.getState(name), headers={'content-type': 'application/json'})
            print(response.text)
            try:
                toUpdate.append([name, eval(response.text)["move"]])
            except:
                with open('out.json', 'w') as out:
                    out.write(str(data))
                sys.exit(0)

        for info in toUpdate:
            state.move(info[0], info[1])
        
        state.kill()
        state.checkFood()
        state.state["turn"] += 1
        #sys.exit(0)
        #TODO: update snakes dictionary to remove dead snakes
        print(state.state)
        print()


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
