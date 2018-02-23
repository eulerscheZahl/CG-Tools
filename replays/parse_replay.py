import requests
import json

from . import code4life, the_great_escape

def get_players(data):
    return [d['codingamer']['pseudo'] if 'codingamer' in d else d['arenaboss']['nickname'] if 'arenaboss' in d else 'defaultAI' for d in data['agents']]

def load_replay(id):
    try:
        r = requests.post('https://www.codingame.com/services/gameResultRemoteService/findByGameId', json = [id, None], timeout=10)
        #f = open('/home/eulerschezahl/test.json', 'r+')
        #data = json.loads(f.read())
    except:
        return 'failed to load'
    data = r.json()
    game = data['success']['frames'][0]['view']
    if 'Roche' in game: return code4life.parse(data['success'])
    if 'TheGreatEscape' in game: return the_great_escape.parse(data['success'])
    raise Exception('game not supported: ' + game.split('\n')[1])
