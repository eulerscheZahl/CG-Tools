from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.defaulttags import register

from . import parse_replay

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def split_line(value):
    return value.strip().replace('\n', '\\n')

def analyze(request):
    replay_id = request.GET.get('id', None)
    if not replay_id: return render(request, 'replay_analyze.html', {'replay_id':None})
    try:
        data = parse_replay.load_replay(replay_id)
    except Exception as ex:
        return HttpResponse(ex.args[0])
    return render(request, 'replay_analyze.html', {'replay_id':replay_id, 'data':data})

def reprod(request):
    replay_id = request.GET.get('id', None)
    if not replay_id: return render(request, 'replay_reprod.html', {'replay_id':None})
    try:
        data = parse_replay.reproduce_replay(replay_id)
        actions = data['actions']
        game = data['game']
    except Exception as ex:
        return HttpResponse(ex.args[0])
    return render(request, 'replay_reprod.html', {'replay_id':replay_id, 'actions':sorted(actions.items())})
