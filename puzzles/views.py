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

@register.filter
def clean_html(html):
    open = html.count('<div')
    close = html.count('</div')
    return '<div>' * max(0, close-open) + html + '</div>' * max(0, open-close)

def index(request):
    categories = set(['ANY'])
    for puzzle in Puzzle.objects.all():
        data = json.loads(puzzle.puzzle)['success']
        categories.add(data['type'])
    categories = sorted(list(categories))
    if 'q' in request.GET:
        search = request.GET['q']
        cat = request.GET.get('category', 'ANY')
        data = puzzle_manager.search(search, cat)
        if len(data) > 1:
            data.sort(key=lambda x: -x['score'])
        return render(request, 'puzzle_base.html', {'search':search, 'data':data, 'categories':categories})
    return render(request, 'puzzle_base.html', {'search':None, 'categories':categories})

@csrf_exempt
def update(request):
    handles = request.POST['handles']
    for h in handles.split():
        puzzle_manager.update(h)
    return HttpResponse('updated successfully')
