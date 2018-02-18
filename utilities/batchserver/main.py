"""Server to rapidly simulate games to determine loss trends"""

import os, glob, json, requests, shutil
from optparse import OptionParser 
from State import State


def runGame(gameCounter, outputDirectory, numFood, snakesFile):

    snakeUrls = []
    with open(snakesFile) as f:
        snakeUrls = list(filter(None, f.read().split("\n"))) # strip out blank lines

    snakes = {}
    differentiationCounter = 0
    for url in snakeUrls:
        response = requests.post(url + "/start", data=json.dumps({"width": 20, "height": 20, "game_id": "gameid"}), headers={'content-type': 'application/json'})
        name = eval(response.text)["name"]
        while name in snakes: # add arbitrary number if names are same
            name = eval(response.text)["name"] + str(differentiationCounter)
            differentiationCounter += 1
        snakes[name] = url + "/move" # assumption is URLs are not /move specific

    state = State(20, 20, list(snakes.keys()), numFood)

    data = []
    data.append(json.dumps(state.state)) # puts state dict in json format

    end = 1
    if len(snakeUrls) == 1: # if solo game
        end = 0

    counter = 0
    while(len(snakes) > end):
        
        toUpdate = []
        for name in snakes:
            response = requests.post(snakes[name], data=state.getPersonalizedState(name), headers={'content-type': 'application/json'})            
            if response.headers.get('content-type') == 'application/json':
                toUpdate.append([name, response.json()["move"]])  
            else:
                # this is not as good as moving same direction but adding
                # that functionality would need a bunch of other machinery
                # and ideally we shouldn't be getting errors at all
                toUpdate.append([name, "up"])
                print(name + " DID NOT RESPOND - MOVING UP")

        if(counter % 10 == 0): # arbitrary counter to display game progress
            print("turn: " + str(counter))
        counter += 1

        for info in toUpdate: # update them here to prevent changing state while processing
            state.move(info[0], info[1])
        
        for name in state.updateState(): # remove dead snakes
            snakes.pop(name)
            
        data.append(json.dumps(state.state))

    printGame(outputDirectory, "game" + str(gameCounter).zfill(3) + ".json", data)


def printGame(dir, filename, data):
    with open(dir + "/" + filename, "w") as out:
        # here we create a json array with our separate json dicts
        out.write("[")
        out.write(",\n".join(data))
        out.write("]")


## Accept command inputs ##
# -d 'directory for game outcomes'
# -f 'number of food items at any one time'
# -g 'number of games to run'
# -s 'file containing urls to snakes'

def printError(option, parser):
    print("Type 'python main.py -h' to get help")
    parser.error(option + " not given")

def main():
    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="outputDirectory", help="Output directory for saved game.json files")
    parser.add_option("-f", "--food", dest="numFood", help="Amount of food on board at any given time")
    parser.add_option("-s", "--snakes", dest="snakeFile", help="File containing snake URLs")
    parser.add_option("-g", "--games", dest="numGames", help="Number of games to simulate")
    options, _ = parser.parse_args()

    if not options.outputDirectory:
        printError("Output directory", parser)
    elif not options.numFood:
        printError("Amount of food", parser)
    elif not options.snakeFile:
        printError("Snake file", parser)
    elif not options.numGames:
        printError("Number of games", parser)

    dirName = options.outputDirectory
    if os.path.exists(dirName):
        for file in glob.glob(dirName + "/game*.json"):
            os.remove(file)
    else:
        os.makedirs(options.outputDirectory)

    for gameNum in range(1, int(options.numGames) + 1):
        runGame(gameNum, options.outputDirectory, int(options.numFood), options.snakeFile)

if __name__ == '__main__':
    main()