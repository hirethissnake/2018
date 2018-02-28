"""
Team SneakySnake's Battlesnake implementation.
Responds to POST /start and POST /move.
"""

import os
import time
from bottle import request, route, post, run, static_file
from app.Game import Game

gameDict = {}
VERBOSE = True

def log(msg, level):
    """
    Provides easy logging of notifications, warnings, and errors.

    ### Levels:
    0 - notifications,
    1 - warning,
    2 - critical error
    """
    levels = [0, 1, 2]
    # Default text color, yellow, red
    colors = ['\033[0m', '\033[93m', '\033[91m']

    # default to level 0
    if level not in levels:
        level = 0

    # Print text in colored version, then default color
    print('{}{}{}'.format(colors[level], msg, colors[0]))


def emergencyStart(gameId, height, width):
    """
    Start a game in the middle of it happening.
    """
    log('Emergency game start', 1)
    data = {
        'height': height,
        'width': width
    }
    battle = Game(data)
    gameDict[gameId] = battle


def getGameDecisions(currentGame):
    """
    Gets the next move and taunt from the game given by currentGame.
    Requires currentGame to exist in gameDict.

    returns: (str, str) - next move, taunt
    """
    # Default move and taunt
    nextMove = 'up'
    nextTaunt = 'oh_noes!'
    battle = gameDict[currentGame]
    # Update Game with new game state
    startTime = time.time()

    # Request next move
    try:
        nextMove = battle.getNextMove()
        nextTaunt = battle.getTaunt()
    except Exception as e:
        log('ERROR: {}'.format(e), 2)

    if VERBOSE:
        endTime = time.time()
        log('Processing time: {} ms'.format((endTime - startTime) * 1000), 0)
        log('Move chosen: {}'.format(nextMove), 0)

    return (nextMove, nextTaunt)


@route('/static/<path:path>')
def static(path):
    """
    Provides access to static files such as images.
    """
    return static_file(path, root='static/')


@post('/start')
def start():
    """
    Respond to POST /start with important details like what our snake looks
    like, and what our taunt is.
    """
    data = request.json
    log('Beginning new game', 1)
    if VERBOSE: log(data, 0)

    #Create a game object with the data given, add it to the list of games
    game_id = data['game_id']
    battle = Game(data)
    gameDict[game_id] = battle

    head_url = '%s://%s/static/head.png' % (
        request.urlparts.scheme,
        request.urlparts.netloc
    )

    sendingData = {
        'color': '#FFEBD0',
        'taunt': battle.getTaunt(),
        'head_url': head_url,
        'name': 'SneakySnake',
        'head_type': 'tongue',
        'tail_type': 'curled'
    }

    return sendingData


@post('/move')
def move():
    """
    Respond to POST /move with an adequate choice of movement.
    """
    data = request.json
    currentGame = None

    log('We received a move request.', 0)
    if VERBOSE: log(data, 0)

    if 'game_id' in data:
        currentGame = data['game_id']
    else:
        log('No game_id in request, making no move.', 1)
        return

    # get currentGame from gameDict
    if currentGame in gameDict:
        battle = gameDict[currentGame]
        battle.update(data)
    else:
        # Handle missing games gracefully
        log('ERROR: Received request for game that does not exist\n' +
        'Running emergency game start routine to get best-guess move', 2)

        emergencyStart(currentGame, data['height'], data['width'])
        battle = gameDict[currentGame]

    nextMove, nextTaunt = getGameDecisions(currentGame)
    sendingData = {
        'move': nextMove,
        'taunt': nextTaunt
    }

    return sendingData


if __name__ == '__main__':
    run(host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
