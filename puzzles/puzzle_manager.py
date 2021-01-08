import json
import requests

from .models import Puzzle

def field_search(puzzles, dict, score):
    for puzzle in puzzles.values_list('handle', flat=True):
        dict[puzzle] += score

def search(search_text, search_category, search_title, search_statement,
           search_tests, search_comments, search_tags, search_author):
    result = []
    handles = list(Puzzle.objects.all().values_list('handle', flat=True))
    handle_scores = dict.fromkeys(handles, 0)

    for search in search_text.split():
        sub_scores = dict.fromkeys(handles, 0)
        query = Puzzle.objects.all()
        if search_category != 'ANY': query = Puzzle.objects.filter(puzzleType=search_category)

        if search_title: field_search(query.filter(title__icontains=search), sub_scores, 10)
        if search_statement:
            field_search(query.filter(inputDescription__icontains=search), sub_scores, 3)
            field_search(query.filter(outputDescription__icontains=search), sub_scores, 2)
            field_search(query.filter(constraints__icontains=search), sub_scores, 2)
            field_search(query.filter(statement__icontains=search), sub_scores, 1)
        if search_tests: field_search(query.filter(testCases__icontains=search), sub_scores, 1)
        if search_tags: field_search(query.filter(topics__icontains=search), sub_scores, 1)
        if search_comments: field_search(query.filter(commentText__icontains=search), sub_scores, 1)
        if search_author: field_search(query.filter(author__icontains=search), sub_scores, 1)

    for handle in sub_scores:
        if handle not in handle_scores: continue
        if sub_scores[handle] == 0: del handle_scores[handle]
        else: handle_scores[handle] += sub_scores[handle]

    handles = list(handle_scores.keys())
    puzzles = Puzzle.objects.filter(handle__in=handles).values('handle', 'title', 'statementHTML', 'puzzleType', 'author')
    for puzzle in puzzles:
        result.append({
            'title': puzzle['title'],
            'url': 'https://www.codingame.com/contribute/view/' + puzzle['handle'],
            'statement': puzzle['statementHTML'],
            'type': puzzle['puzzleType'],
            'author': puzzle['author'],
            'score': handle_scores[puzzle['handle']]
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
