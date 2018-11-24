import json
import requests

from .models import Puzzle

def search(search_text):
    result = []
    for puzzle in Puzzle.objects.all():
        data = json.loads(puzzle.puzzle)['success']
        hit = True
        for s in search_text.split():
            subHit = False
            for category in ['inputDescription', 'outputDescription', 'constraints', 'statement', 'title']:
                if category in data['lastVersion']['data'] and s in data['lastVersion']['data'][category].lower(): subHit = True
            if not subHit: hit = False
        if hit:
            data['lastVersion']['statementHTML'] += '</div>'
            result.append({
                'title': data['title'],
                'url': 'https://www.codingame.com/contribute/view/' + puzzle.handle,
                'statement': data['lastVersion']['statementHTML'],
                'type': data['type'],
                'author': data['nickname'] if 'nickname' in data else 'unknown',
            })
    return result

def update(handle):
    puzzle = Puzzle.objects.filter(handle=handle).first()
    if puzzle == None:
        url = 'https://www.codingame.com/services/ContributionRemoteService/getContribution'
        r = requests.post(url, json=[handle,True])
        puzzle = Puzzle(handle=handle, puzzle=json.dumps(r.json()))
        puzzle.save()
