from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template.defaulttags import register
import json
import requests
from datetime import datetime


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_replay(replays, user):
    return replays.get(str(user['agentId']))


@register.filter
def get_replay_by_id(replays, replay_id):
    return replays.get(str(replay_id))


@register.filter
def get_matches(groups, user):
    agentId = user['agentId']
    for group in groups:
        if agentId in group:
            result = group[:]
            result.remove(agentId)
            return result
    return []


@register.filter
def get_user(users, id):
    for user in users:
        if user['agentId'] == id:
            return user
    return None


@register.filter
def get_time(timestamp):
    return datetime.utcfromtimestamp(timestamp//1000).strftime('%Y-%m-%d')


def index(request):
    game = None
    replayGroups = None
    botReplays = None
    users = None
    if 'game' in request.GET:
        game = request.GET['game']
        leaderboard = Leaderboard.objects.filter(game=game).first()
        replayGroups = json.loads(leaderboard.replayGroups)
        botReplays = json.loads(leaderboard.botReplays)
        url = 'https://www.codingame.com/services/Leaderboards/getFilteredPuzzleLeaderboard'
        data = [game, None, "global", {
            "active": True, "column": "LEAGUE", "filter": "legend"}]
        r = requests.post(url, json=data).json()
        users = r['users']
        users = users[:100]
    games = Leaderboard.objects.all().values_list("game", flat=True)

    return render(request, 'leaderboards.html', {'game': game, 'users': users, 'replayGroups': replayGroups, 'botReplays': botReplays, 'games': games})


@csrf_exempt
def update(request):
    game = request.POST['game']
    botReplays = request.POST['botReplays']
    replayGroups = request.POST['replayGroups']
    Leaderboard.updateEntry(game, botReplays, replayGroups)
    return HttpResponse('updated successfully')
