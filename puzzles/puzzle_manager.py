import json
import requests

from .models import Puzzle

def search(search_text):
    result = []
    for puzzle in Puzzle.objects.all():
        hit = False
        for s in search_text.split():
            if s in puzzle.puzzle.lower(): hit = True
        if hit:
            data = json.loads(puzzle.puzzle)['success']
            data['lastVersion']['statementHTML'] += '</div>'
            print(data['title'])
            result.append({
                'title':data['title'],
                'url': 'https://www.codingame.com/contribute/view/' + puzzle.handle,
                'statement':data['lastVersion']['statementHTML']
            })
    return result

def update(handle):
    puzzle = Puzzle.objects.filter(handle=handle).first()
    if puzzle == None:
        url = 'https://www.codingame.com/services/ContributionRemoteService/getContribution'
        r = requests.post(url, json=[handle,True])
        puzzle = Puzzle(handle=handle, puzzle=json.dumps(r.json()))
        puzzle.save()
