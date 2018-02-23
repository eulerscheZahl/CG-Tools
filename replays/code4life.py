import json

from . import parse_replay

def parse(data):
    players = parse_replay.get_players(data)
    data = data['frames']
    init = data[0]['view'].split('\n')
    project_count = int(init[4])
    projects = [str(project_count)]
    for i in range(project_count):
        projects.append(init[i+5])
    samples = []
    game_input = [{'player':players[0], 'game':[], 'init':[]}, {'player': players[1], 'game':[], 'init':[]}]
    game0 = game_input[0]['game']
    game1 = game_input[1]['game']
    user_output = {}
    for p in projects:
        game_input[0]['init'].append(p)
        game_input[1]['init'].append(p)
    for frame in range(len(data)):
        if 'stdout' in data[frame]:
            user_output[frame] = data[frame]['stdout']
        view = data[frame]['view']
        if data[frame]['keyframe']:
            input = view.split('\n')
            game0.append({'round':frame, 'input':[]})
            game1.append({'round':frame, 'input':[]})
            input0 = game0[-1]['input']
            input1 = game1[-1]['input']
            offset = 1 if frame > 0 else 6 + project_count
            for player in range(2):
                line = input[player + offset].split()
                target = line[0]
                source = line[1]
                eta = line[2]
                mols = ' '.join(line[5:10])
                exp = ' '.join(line[10:15])
                score = '0' if len(line) < 16 else line[15]
                input0.append(' '.join([target, eta, score, mols, exp]))
            input1.append(input0[-1])
            input1.append(input0[-2])
            input0.append(input[offset+2]) # shared molecules
            input1.append(input[offset+2])
            actions = 0 if input[offset+3].strip() == '' else int(input[offset+3])
            for a in range(actions):
                action = input[offset+4+a].split()
                if action[0] == '0': samples.append(Sample(action[1], ' '.join(action[2:7]), action[7], action[8], action[9], action[10]))
                elif action[0] == '4':
                    sample = next(s for s in samples if s.id == action[1])
                    sample.diagnosed = True
                elif action[0] == '2':
                    sample = next(s for s in samples if s.id == action[1])
                    sample.player = '-1'
                elif action[0] == '5':
                    sample = next(s for s in samples if s.id == action[1])
                    samples.remove(sample)
                elif action[0] == '1':
                    sample = next(s for s in samples if s.id == action[1])
                    sample.player = action[2]
            input0.append(str(len(samples)))
            input1.append(str(len(samples)))
            for s in samples:
                input0.append(str(s))
                input1.append(s.opponent())
    return {'game': 'code4life', 'input':game_input, 'output':user_output}

class Sample:
    def __init__(self, id, cost, rank, health, expert, player):
        self.id = id
        self.cost = cost
        self.rank = str(int(rank)+1)
        self.health = health
        self.expert = expert
        self.player = player
        self.diagnosed = False

    def __str__(self):
        if self.diagnosed:
            return ' '.join([self.id, self.player, self.rank, self.expert, self.health, self.cost])
        return ' '.join([self.id, self.player, self.rank, '0', '-1', '-1 -1 -1 -1 -1'])

    def opponent(self):
        player = self.player
        if player == '1': player = '0'
        elif player == '0': player = '1'
        if self.diagnosed:
            return ' '.join([self.id, player, self.rank, self.expert, self.health, self.cost])
        return ' '.join([self.id, player, self.rank, '0', '-1', '-1 -1 -1 -1 -1'])
