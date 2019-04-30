import json
import requests

from .models import Puzzle

def search(search_text):
    result = []
    for puzzle in Puzzle.objects.all():
        data = json.loads(puzzle.puzzle)['success']
        hit = True
        for s in search_text.lower().split():
            subHit = False
            for category in ['inputDescription', 'outputDescription', 'constraints', 'statement', 'title']:
                if category in data['lastVersion']['data'] and s in data['lastVersion']['data'][category].lower(): subHit = True
            for test in data['lastVersion']['data']['testCases']:
                if s in str(test['title']).lower(): subHit = True
            if 'topics' in data['lastVersion']['data']: # check for matches in the tags
                for tag in data['lastVersion']['data']['topics']:
                    for language in tag['labelMap'].values():
                        if s in str(language).lower(): subHit = True
            if puzzle.comments != '':
                for comment in json.loads(puzzle.comments):
                    if s in comment['content'].lower(): subHit = True
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
    if puzzle.comments == '':
        comments = []
        url = 'https://www.codingame.com/services/CommentRemoteService/getFirstLevelComments'
        url2 = 'https://www.codingame.com/services/CommentRemoteService/getSecondLevelComments'
        r = requests.post(url, json=[None,json.loads(puzzle.puzzle)['success']['commentableId']])
        for comment in r.json()['success']:
            comments.append(comment)
            if not 'parentCommentId' in comment and comment['responseCount'] > 1:
                r = requests.post(url2, json=[None,comment['commentId']])
                for comment2 in r.json()['success']:
                    comments.append(comment2)
        commentsUnique = []
        for c in comments:
            if not any(c['commentId'] == c2['commentId'] for c2 in commentsUnique):
                commentsUnique.append(c)
        puzzle.comments = json.dumps(commentsUnique)
        puzzle.save()
        
