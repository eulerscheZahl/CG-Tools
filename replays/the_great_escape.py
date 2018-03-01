import json

from . import parse_replay

def parse(data):
    players = parse_replay.get_players(data)
    data = data['frames']
    init = data[0]['view'].split('\n')[2] + ' '
    game_input = [{'player':p, 'game':[], 'init':[init + str(players.index(p))]} for p in players]
    walls = []

    user_output = {}
    for frame in range(len(data) - 1):
        if 'stdout' in data[frame]:
            user_output[frame] = data[frame]['stdout']
        view = data[frame]['view']
        input = view.split('\n')
        agent_id = data[frame+1]['agentId']
        offset = 3 if frame == 0 else 1
        round = []
        for i in range(len(players)):
            round.append(' '.join(input[2*i+offset].split()[:3]))
        if len(players) == 3: offset += 1
        wall_count = int(input[2+offset+len(players)])
        for i in range(wall_count):
            walls.append(input[3+offset+len(players)+i])
        round.append(str(len(walls)))
        for w in walls:
            round.append(w)
        game_input[agent_id]['game'].append({'round':frame, 'input':round})

    return {'game': 'the great escape', 'input':game_input, 'output':user_output}
