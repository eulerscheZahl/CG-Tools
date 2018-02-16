from django.http import HttpResponse
from django.shortcuts import render

from . import parse_replay

def index(request):
    return HttpResponse("start")

def detail(request, replay_id):
    data = parse_replay.load_replay(replay_id)
    html = '<h1>' + data['game'] + '</h1>\n'
    input_data = data['input']
    html += '<table>\n<tr>\n'
    for player in input_data:
        html += '<th>' + player['player'] + '</th>\n'
    html += '</tr>\n'
    for player in input_data:
        html += '<td>\n'
        for round in player['game']:
            html += '<h3>round ' + str(round['round']) + '</h3>\n'
            for line in round['input']:
                html += line + '</br>\n'
        html += '</td>\n'
    html += '</table>'

    return HttpResponse(html)

"""<table style="width:100%">
  <tr>
    <th>Firstname</th>
    <th>Lastname</th>
    <th>Age</th>
  </tr>
  <tr>
    <td>Jill</td>
    <td>Smith</td>
    <td>50</td>
  </tr>
  <tr>
    <td>Eve</td>
    <td>Jackson</td>
    <td>94</td>
  </tr>
</table>"""
