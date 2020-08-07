import json
import requests

from .models import Puzzle

def search(search_text, search_category, search_title, search_statement,
           search_tests, search_comments, search_tags, search_author):
    result = []
    for puzzle in Puzzle.objects.all():
        data = json.loads(puzzle.puzzle)['success']
        if data['type'] != search_category and search_category != 'ANY': continue
        author = data['nickname'] if 'nickname' in data else 'unknown'
        hit = True
        score = 0
        for s in search_text.lower().split():
            sub_score = 0
            for category in ['inputDescription', 'outputDescription', 'constraints', 'statement', 'title']:
                if category in data['lastVersion']['data'] and s in data['lastVersion']['data'][category].lower():
                    if search_title and category == 'title': sub_score += 10
                    if search_statement and category == 'inputDescription': sub_score += 3
                    if search_statement and category == 'outputDescription': sub_score += 2
                    if search_statement and category == 'constraints': sub_score += 2
            if search_tests and 'testCases' in data['lastVersion']['data']:
                for test in data['lastVersion']['data']['testCases']:
                    if s in str(test['title']).lower() or s in str(test['testIn']).lower() or s in str(test['testOut']).lower():
                        sub_score += 1
            if search_tags and 'topics' in data['lastVersion']['data']: # check for matches in the tags
                for tag in data['lastVersion']['data']['topics']:
                    for language in tag['labelMap'].values():
                        if s in str(language).lower():
                            sub_score += 1
            if search_comments and puzzle.comments != '':
                for comment in json.loads(puzzle.comments):
                    if s in comment['content'].lower():
                        sub_score += 1
            if search_author and s in author.lower(): sub_score += 1
            if sub_score == 0: hit = False
            score += sub_score
        if hit:
            if 'statementHTML' in data['lastVersion']: # classic puzzle
                statement = data['lastVersion']['statementHTML'] + '</div>'
            elif 'statement' in data['lastVersion']['data']: # classic puzzle
                statement = data['lastVersion']['data']['statement'] + '</div>'
            else: # interactive
                statement = data['lastVersion']['data']['levelParams']
                key = sorted(list(statement.keys()))[-1]
                statement = statement[key]['statements']['2']
            result.append({
                'title': data['title'],
                'url': 'https://www.codingame.com/contribute/view/' + puzzle.handle,
                'statement': statement,
                'type': data['type'],
                'author': author,
                'score': score
            })
    return result

def update(handle):
    puzzle = Puzzle.objects.filter(handle=handle).first()
    if puzzle == None:
        url = 'https://www.codingame.com/services/ContributionRemoteService/findContribution'
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
