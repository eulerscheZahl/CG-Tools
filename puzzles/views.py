import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.defaulttags import register
from django.views.decorators.csrf import csrf_exempt

from . import puzzle_manager
from .models import *


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def index(request):
    categories = Puzzle.objects.all().values_list(
        "puzzleType", flat=True).distinct()
    categories = list(categories)
    categories.append("ANY")
    categories.sort()
    if 'q' in request.GET:
        search = request.GET['q']
        cat = request.GET.get('category', 'ANY')
        title = 'title' in request.GET
        statement = 'statement' in request.GET
        tests = 'tests' in request.GET
        comments = 'comments' in request.GET
        tags = 'tags' in request.GET
        author = 'author' in request.GET
        data = puzzle_manager.search(
            search, cat, title, statement, tests, comments, tags, author)
        if len(data) > 1:
            data.sort(key=lambda x: -x['score'])
        return render(request, 'puzzle_search.html', {'search': search, 'data': data, 'categories': categories,
                                                      'title': title, 'statement': statement, 'tests': tests,
                                                      'comments': comments, 'tags': tags, 'author': author})
    return render(request, 'puzzle_search.html',
                  {'search': None, 'categories': categories, 'title': True, 'statement': True, 'tests': True,
                   'comments': True, 'tags': True, 'author': True}
                  )


def stats(request):
    times = {}
    data = []
    for puzzle in Puzzle.objects.all():
        if not puzzle.puzzleType in times:
            times[puzzle.puzzleType] = []
        try:
            times[puzzle.puzzleType].append(json.loads(puzzle.puzzle)[
                                            'lastVersion']['autocloseTime'])
            data.append({'x': json.loads(puzzle.puzzle)[
                        'lastVersion']['autocloseTime'], 'y': 1})
        except:
            pass

    return render(request, 'puzzle_stats.html', {'data': data})


@csrf_exempt
def update(request):
    handles = request.POST['handles']
    existingHandles = Puzzle.objects.all().values_list("handle", flat=True).distinct()
    for h in handles.split():
        if h not in existingHandles:
            puzzle_manager.update(h)
    return HttpResponse('updated successfully')
