"""Server to rapidly simulate games to determine loss trends"""

from State import State
import sys


def runGame():
    state = State(20, 20, 1, 1)

    allDead = False
    while(not allDead):
        state.incrementState(stepSnakes(state))
        state.kill()
        if state.numAlive() == 0:
            allDead = True

    #print(state.getState())

def printGames(games, p, m):
    #given games[], print to file/directory p
    #if m(bool), print each game to a different file
    return

def stepSnakes(gameState):
    #send gameState to each snake and waits for a response
    #retruns an array of moves
    return []

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
    if len(sys.argv) < 2 or len(sys.argv) > 2 or not sys.argv[1].isdigit():
        raise ValueError('Invalid arguments')
    for i in range(0, int(sys.argv[1])):
        runGame()
