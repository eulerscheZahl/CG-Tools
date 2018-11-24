from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.defaulttags import register
from django.views.decorators.csrf import csrf_exempt

from . import puzzle_manager

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def index(request):
    if 'search' in request.POST:
        return redirect('detail', search=request.POST['search'])
    return render(request, 'puzzle_base.html', {'search':None})

def post(request):
    print(request)

def detail(request, search):
    if 'search' in request.POST:
        return redirect('detail', search=request.POST['search'])
    try:
        data = puzzle_manager.search(search)
    except Exception as ex:
        return HttpResponse(ex.args[0])
    return render(request, 'puzzle_base.html', {'search':search, 'data':data})

@csrf_exempt
def update(request):
    handles = request.POST['handles']
    for h in handles.split():
        puzzle_manager.update(h)
    return HttpResponse('updated successfully')
