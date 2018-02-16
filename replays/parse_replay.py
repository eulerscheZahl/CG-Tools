import requests
import json

from . import code4life

def get_players(data):
    return [d['codingamer']['pseudo'] if 'codingamer' in d else d['arenaboss']['nickname'] for d in data['agents']]

def load_replay(id):
    try:
        r = requests.post('https://www.codingame.com/services/gameResultRemoteService/findByGameId', json = [id, None], timeout=10)
    except:
        return 'failed to load'
    data = r.json()
    game = data['success']['frames'][0]['view']
    if 'Roche' in game: return code4life.parse(data['success'])
    raise Exception('game not supported: ' + game.split('\n')[1])
