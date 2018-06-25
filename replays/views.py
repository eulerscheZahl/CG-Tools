from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.defaulttags import register

from . import parse_replay

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def index(request):
    if 'id' in request.POST:
        return redirect('detail', replay_id=request.POST['id'])
    return render(request, 'base.html', {'replay_id':None})

def post(request):
    print(request)

def detail(request, replay_id):
    if 'id' in request.POST:
        return redirect('detail', replay_id=request.POST['id'])
    try:
        data = parse_replay.load_replay(replay_id)
    except Exception as ex:
        return HttpResponse(ex.args[0])
    return render(request, 'base.html', {'replay_id':replay_id, 'data':data})

def reprod(request, replay_id):
    if 'id' in request.POST:
        return redirect('reprod', replay_id=request.POST['id'])
    try:
        data = parse_replay.reproduce_replay(replay_id)
        actions = data['actions']
        game = data['game']
    except Exception as ex:
        return HttpResponse(ex.args[0])
    return render(request, 'reprod.html', {'replay_id':replay_id, 'actions':sorted(actions.items())})
