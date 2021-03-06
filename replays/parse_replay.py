import requests
import json

from . import code4life, the_great_escape, tic_tac_toe

def get_players(data):
    return [d['codingamer']['pseudo'] if 'codingamer' in d else d['arenaboss']['nickname'] if 'arenaboss' in d else 'defaultAI' for d in data['agents']]

def get_data(id):
    try:
        r = requests.post('https://www.codingame.com/services/gameResultRemoteService/findByGameId', json = [id, None], timeout=10)
        data = r.json()
        # f = open('/home/eulerschezahl/uttt.json', 'r+')
        # data = json.loads(f.read())
    except:
        return 'failed to load'
    return data

def load_replay(id):
    data = get_data(id)
    game = data['frames'][0]['view']
    if 'Roche' in game: return code4life.parse(data)
    if 'TheGreatEscape' in game: return the_great_escape.parse(data)

    # new framework doesn't give the name, try to detect it by filenames instead
    # not happy about that solution :(
    s = json.dumps(data)
    if 'circle.png' in s and 'cross.png' in s:
        return tic_tac_toe.parse(data)
    raise Exception(s)

def reproduce_replay(id):
    data = get_data(id)
    game = data['frames'][0]['view']
    actions = {}
    for frame in data['frames']:
        if 'agentId' not in frame or 'stdout' not in frame: continue
        agent = frame['agentId']
        stdout = frame['stdout'].replace('\\n', '')
        if agent not in actions: actions[agent] = []
        if stdout != '': actions[agent].append(stdout)
    return { 'game':game, 'actions':actions }
