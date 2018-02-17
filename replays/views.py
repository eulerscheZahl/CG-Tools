from django.http import HttpResponse
from django.shortcuts import render

from . import parse_replay

def index(request):
    return HttpResponse("start")

def detail(request, replay_id):
    try:
        data = parse_replay.load_replay(replay_id)
        html = '<h1>' + data['game'] + '</h1>\n'
        html += '<iframe src="https://www.codingame.com/replay/' + str(replay_id) + '" height="700" width="700"></iframe></br>\n'
        input_data = data['input']
        html += '<table>\n<tr>\n'
        for player in input_data:
            html += '<th>' + player['player'] + '</th>\n'
        html += '</tr>\n'
        for player in input_data:
            html += '<td>\n'
            html += '<h3>init</h3>\n'
            print(player['init'])
            for init in player['init']:
                html += init + '</br>\n'
            html += '<div style="overflow-y: scroll; height:400px;">'
            for round in player['game']:
                html += '<h3>round ' + str(round['round']) + '</h3>\n'
                for line in round['input']:
                    html += line + '</br>\n'
            html += '</div></td>\n'
        html += '</table>'

        return HttpResponse(html)
    except Exception as inst:
        return HttpResponse(inst.args[0])
