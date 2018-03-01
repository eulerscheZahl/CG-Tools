import json

from . import parse_replay

def parse(data):
    players = parse_replay.get_players(data)
    data = data['frames']
    init = ''
    game_input = [{'player':p, 'game':[], 'init':[]} for p in players]

    user_output = {}
    board = Board()
    for frame in range(len(data)):
        if 'stdout' in data[frame]:
            user_output[frame] = data[frame]['stdout']
            parts = data[frame]['stdout'].split()
            agent_id = data[frame]['agentId']
            game_input[agent_id]['game'].append({'round':frame-1, 'input':str(board).split('\n')})
            board.play(int(parts[0]), int(parts[1]), frame)

    return {'game': 'Tic Tac Toe', 'input':game_input, 'output':user_output}

class Board:
    def __init__(self):
        self.grid = [['.'] * 9 for i in range(9)]

    def play(self, x, y, turn):
        grid = self.grid
        player = ['o', 'x'][turn%2]
        grid[x][y] = player
        sub_x = x//3
        sub_y = y//3
        fill = False
        for x_ in range(3):
            if grid[3*sub_x + x_][3*sub_y] == player and \
                grid[3*sub_x + x_][3*sub_y + 1] == player and \
                grid[3*sub_x + x_][3*sub_y + 2] == player:
                fill = True
        for y_ in range(3):
            if grid[3*sub_x][3*sub_y + y_] == player and \
                grid[3*sub_x + 1][3*sub_y + y_] == player and \
                grid[3*sub_x + 2][3*sub_y + y_] == player:
                fill = True
        if grid[3*sub_x][3*sub_y] == player and \
            grid[3*sub_x + 1][3*sub_y + 1] == player and \
            grid[3*sub_x + 2][3*sub_y + 2] == player:
                fill = True
        if grid[3*sub_x + 2][3*sub_y] == player and \
            grid[3*sub_x + 1][3*sub_y + 1] == player and \
            grid[3*sub_x][3*sub_y + 2] == player:
                fill = True
        if fill:
            for x_ in range(3):
                for y_ in range(3):
                    grid[3*sub_x + x_][3*sub_y + y_] = player

    def __str__(self):
        result = ''
        for x in range(9):
            result += ''.join([self.grid[x][y] for y in range(9)]) + '\n'
        return result.strip()
