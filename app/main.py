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
    # Default move and taunt
    nextMove = 'up'
    nextTaunt = 'oh_noes!'
    currentGame = None

    log('We received a move request.', 0)
    if VERBOSE: log(data, 0)

    if 'game_id' in data:
        currentGame = data['game_id']
    else:
        log('No game_id in request', 1)

    # get currentGame from gameDict
    if currentGame in gameDict:
        battle = gameDict[currentGame]
        # Update Game with new game state
        startTime = time.time()
        battle.update(data)
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
    else:
        log('ERROR: Received request for game that does not exist\n' +
        'To avoid collateral damage to other games, responding with default move "up"', 2)

    sendingData = {
        'move': nextMove,
        'taunt': nextTaunt
    }

    return sendingData

if __name__ == '__main__':
    run(host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
