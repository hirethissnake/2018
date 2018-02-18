"""Server to rapidly simulate games to determine loss trends"""

import sys
import os
import json
import requests
from optparse import OptionParser

from State import State


def runGame(snakesFile, gameCounter, outputDirectory, numFood):
    #TODO:
    # add robusteness and proper command system
    # randomly spawn right amount of food

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

    state = State(20, 20, list(snakes.keys()), numFood)

    data = []
    data.append(json.dumps(state.state))

    counter = 0
    while(len(snakes) > 1):        
        
        toUpdate = []
        for name in snakes:
            response = requests.post(snakes[name], data=state.getState(name), headers={'content-type': 'application/json'}).text            
            if("DOCTYPE HTML" not in response):
                toUpdate.append([name, eval(response)["move"]])  
            else:
                toUpdate.append([name, "up"])     
                print(name + " DID NOT RESPOND - MOVING UP") 

        if(counter % 10 == 0):
            print("turn: " + str(counter))
        counter += 1

        for info in toUpdate:
            state.move(info[0], info[1])
        
        for name in state.updateState():
            snakes.pop(name)
            
        data.append(json.dumps(state.state))

    printGame(outputDirectory, "game" + str(gameCounter).zfill(3) + ".json", data)
    return gameCounter + 1


def printGame(dir, filename, data):
    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(dir + "/" + filename, "w") as out:
        out.write("[")
        out.write(",\n".join(data))
        out.write("]")


## Accept command inputs ##
#-d 'directory for game outcomes'
#-f 'number of food items at any one time'
#-n 'number of games to run'
#-s 'file containing urls to snakes'

def printError(option):
    print("Type 'python main.py -h' to get help")
    parser.error(option + " not given")

if __name__ == '__main__':
    #if len(sys.argv) != 3 or not sys.argv[1].isdigit():
    #    raise ValueError('Invalid arguments')

    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="outputDirectory", help="Output directory for saved game.json files")
    parser.add_option("-f", "--food", dest="numFood", help="Amount of food on board at any given time")
    options, args = parser.parse_args()

    if not options.outputDirectory:
        printError("Output directory")
    elif not options.numFood:
        printError("Amount of food")

    gameCounter = 1
    for i in range(0, int(sys.argv[1])):
        gameCounter = runGame(sys.argv[2], gameCounter, options.outputDirectory, int(options.numFood))