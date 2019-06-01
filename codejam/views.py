from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.defaulttags import register
from os import listdir
import json

from .models import Round, Country, User, RoundResult

@register.filter
def format_time(time):
    return '{}:{:02}:{:02}'.format(time//3600, time//60%60, time%60)

def autocomplete(request):
    if request.is_ajax():
        queryset = User.objects.filter(name__icontains=request.GET.get('search', None))
        list = []
        for i in queryset:
            list.append(i.name)
        data = {
            'list': list,
        }
        return JsonResponse(data)

def index(request):
    if 'search' in request.POST:
        return redirect('detail', search=request.POST['search'])
    return render(request, 'codejam_base.html', {'search':None})

def detail(request, search):
    if 'search' in request.POST:
        if request.POST['search'] == '':
            return render(request, 'codejam_base.html', {'search':None})
        return redirect('detail', search=request.POST['search'])

    user = User.objects.filter(name=search).first()
    if user == None: return render(request, 'codejam_base.html', {'search':None})
    data = RoundResult.objects.filter(user=user).order_by('round__order')
    return render(request, 'codejam_base.html', {'search':search, 'data':data})

@transaction.atomic
def update(request):
    dir = '/home/eulerschezahl/Dokumente/Programmieren/challenges/codejam/2017/'
    year = dir.split('/')[-2]
    for file in listdir(dir):
        with open(dir + file, 'r') as f:
            data = json.loads(f.read())
        parts = file.split('_')
        parts[-1] = year
        round_name = ' '.join(parts)
        round = Round.objects.filter(name=round_name).first()
        if round == None: round = Round.create(round_name)
        for result in data['rows']:
            name = result['n']
            points = result['pts']
            time = result['pen']
            country_name = result['c']
            rank = result['r']
            print(name, points, time, country_name, rank)

            country = Country.objects.filter(name=country_name).first()
            if country == None: country = Country.create(country_name)
            user = User.objects.filter(name=name).first()
            if user == None: user = User.create(name=name, country=country)
            RoundResult.create(round=round, user=user, rank=rank, points=points, time=time)

    return HttpResponse('done')

@transaction.atomic
def update2(request):
    dir = '/home/eulerschezahl/Dokumente/Programmieren/challenges/codejam/google_codejam_stats/client/public/round_data/'
    for round in ['00000000000000cb.json', '0000000000000130.json', '0000000000007706.json', '0000000000007707.json',
                  '0000000000007764.json', '0000000000007765.json', '0000000000007766.json',
                  '0000000000007883.json', '0000000000051635.json', '00000000000516b9.json',
                  '0000000000051705.json', '0000000000051706.json']:
        info = dir + 'info/' + round
        scores = dir + 'scores/' + round
        with open(info, 'r') as f:
            data = json.loads(f.read())
        round_name = data['challenge']['title']
        round = Round.objects.filter(name=round_name).first()
        if round == None: round = Round.create(round_name)
        with open(scores, 'r') as f:
            data = json.loads(f.read())
        for result in data:
            name = result['displayname']
            points = result['score1']
            time = -result['score2'] // 1000000
            country_name = result['country']
            rank = result['rank']
            print(name, points, time, country_name, rank)

            country = Country.objects.filter(name=country_name).first()
            if country == None: country = Country.create(country_name)
            user = User.objects.filter(name=name).first()
            if user == None: user = User.create(name=name, country=country)
            RoundResult.create(round=round, user=user, rank=rank, points=points, time=time)

    return HttpResponse('done')