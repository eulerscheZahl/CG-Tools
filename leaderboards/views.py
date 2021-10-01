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
    user = None
    bots = None
    user_matches = {}
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

    if 'user' in request.GET:
        user = request.GET['user']
        all_bots = json.loads(Leaderboard.objects.filter(
            game='bots_per_user').first().botReplays)
        user_of_bot = {}
        for bot in all_bots:
            for g in all_bots[bot]['bots']:
                for bot_id in all_bots[bot]['bots'][g]:
                    user_of_bot[bot_id] = all_bots[bot]['username']

        bots = all_bots[user]
        for g in bots['bots']:
            user_matches[g] = []
            leaderboard = Leaderboard.objects.filter(game=g).first()
            replayGroups = json.loads(leaderboard.replayGroups)
            botReplays = json.loads(leaderboard.botReplays)
            for bot in bots['bots'][g]:
                bots_matches = {'bot': botReplays[str(bot)], 'partners': {}}
                for group in replayGroups:
                    if bot not in group:
                        continue
                    for gr in group:
                        if user_of_bot[gr] != user_of_bot[bot]:
                            bots_matches['partners'][user_of_bot[gr]
                                                     ] = botReplays[str(gr)]
                user_matches[g].append(bots_matches)

    games = sorted(Leaderboard.objects.all().values_list("game", flat=True))
    games.remove('bots_per_user')

    return render(request, 'leaderboards.html',
                  {'games': games,
                   'game': game, 'users': users, 'replayGroups': replayGroups, 'botReplays': botReplays,
                   'user': user, 'bots': bots, 'user_matches': user_matches})


@csrf_exempt
def update(request):
    game = request.POST['game']
    botReplays = request.POST['botReplays']
    replayGroups = request.POST['replayGroups']
    Leaderboard.updateEntry(game, botReplays, replayGroups)
    return HttpResponse('updated successfully')
