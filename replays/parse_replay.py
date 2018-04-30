import requests
import json

from . import code4life, the_great_escape, tic_tac_toe

def get_players(data):
    return [d['codingamer']['pseudo'] if 'codingamer' in d else d['arenaboss']['nickname'] if 'arenaboss' in d else 'defaultAI' for d in data['agents']]

def load_replay(id):
    try:
        r = requests.post('https://www.codingame.com/services/gameResultRemoteService/findByGameId', json = [id, None], timeout=10)
        data = r.json()
        # f = open('/home/eulerschezahl/uttt.json', 'r+')
        # data = json.loads(f.read())
    except:
        return 'failed to load'
    game = data['success']['frames'][0]['view']
    if 'Roche' in game: return code4life.parse(data['success'])
    if 'TheGreatEscape' in game: return the_great_escape.parse(data['success'])

    # new framework doesn't give the name, try to detect it by filenames instead
    # not happy about that solution :(
    s = json.dumps(data)
    if 'circle.png' in s and 'cross.png' in s:
        return tic_tac_toe.parse(data['success'])
    raise Exception('game not supported: ' + game.split('\n')[1] + '</br></br></br>' + s)
