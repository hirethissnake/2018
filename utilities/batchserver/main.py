"""Server to rapidly simulate games to determine loss trends"""

import sys
import pickle
import json
import time
import requests
from State import State


def runGame(snakesFile):
    #TODO: add health system
    # add robusteness and proper command system
    # randomly spawn right amount of food
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
    counter = 0
    while(len(snakes) > 1):
        
        data.append(json.dumps(state.state))
        
        toUpdate = []
        for name in snakes:
            response = requests.post(snakes[name], data=state.getState(name), headers={'content-type': 'application/json'}).text            
            if("DOCTYPE HTML" not in response):
                toUpdate.append([name, eval(response)["move"]])        

        if(counter % 10 == 0):
            print("turn: " + str(counter))
            counter += 1

        for info in toUpdate:
            state.move(info[0], info[1])
        
        for name in state.kill():
            snakes.pop(name)
            
        state.checkFood()
        state.state["turn"] += 1

    printGame("out.json", data)


def printGame(filename, data):
    with open(filename, "w") as out:
        out.write("[")
        out.write(",\n".join(data))
        out.write("]")


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
