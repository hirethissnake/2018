"""
Team Sneaky Snake Battlesnake implementation.
Responds to POST /start and POST /move.
"""

import os
import time
import bottle
from app.Game import Game

gameDict = {}

@bottle.route('/static/<path:path>')
def static(path):
    """Provides access to static files such as images."""
    return bottle.static_file(path, root='static/')

@bottle.post('/start')
def start():
    """Respond to POST /start with important details like what our snake looks
    like, and what our taunt is."""
    data = bottle.request.json

    print('We have begun a new game!')
    print(data)

    #Create a game object with the data given
    game_id = data['game_id']
    battle = Game(data)
    #Enter the game into the gameDict with the key value set to its id
    gameDict[game_id] = battle

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    sendingData = {
        'color': '#FFEBD0',
        'taunt': 'SSssssSSSsSSsssS',
        'head_url': head_url,
        'name': 'SneakySnake',
        'head_type': 'tongue',
        'tail_type': 'curled'
    }

    # log and return
    return sendingData

@bottle.post('/move')
def move():
    """Respond to POST /move with an adequate choice of movement."""
    data = bottle.request.json

    print('We have received a move')
    print(data)

    # get game_id
    if 'game_id' in data:
        curGame = data['game_id']
    else:
        print('Data missing game_id')

    # get curGame from gameDict
    if curGame in gameDict:
        battle = gameDict[curGame]
        #Update the game with new gamestate
        start = time.time()
        battle.update(data)
        #Request next best move
        nextMove = battle.getNextMove()
        #nextTaunt = battle.getTaunt()
        print('--- %s seconds ---' % (time.time() - start))
    else:
        print('ERROR: Received request for game that does not exist')
        print('To avoid collateral damage to other games, responding with default move')
        nextMove = 'up'

    sendingData = {
        'move': nextMove,
        'taunt': 'please no'
    }

    return sendingData


# Expose WSGI app (so gunicorn can find it)
APPLICATION = bottle.default_app()
if __name__ == '__main__':
    bottle.run(APPLICATION, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
