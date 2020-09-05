import json
import requests

from .models import Puzzle

def search(search_text, search_category, search_title, search_statement,
           search_tests, search_comments, search_tags, search_author):
    result = []
    for puzzle in Puzzle.objects.all():
        if puzzle.puzzleType != search_category and search_category != 'ANY': continue
        hit = True
        score = 0
        for s in search_text.lower().split():
            sub_score = 0
            if search_title and s in puzzle.title.lower(): sub_score += 10
            if search_statement:
                if s in puzzle.inputDescription.lower(): sub_score += 3
                if s in puzzle.outputDescription.lower(): sub_score += 2
                if s in puzzle.constraints.lower(): sub_score += 2
                if s in puzzle.statement.lower(): sub_score += 1
            if search_tests and s in puzzle.testCases.lower(): sub_score += 1
            if search_tags and s in puzzle.topics.lower(): sub_score += 1
            if search_comments and s in puzzle.commentText: sub_score += 1
            if search_author and s in puzzle.author.lower(): sub_score += 1
            if sub_score == 0: hit = False
            score += sub_score
        if hit:
            result.append({
                'title': puzzle.title,
                'url': 'https://www.codingame.com/contribute/view/' + puzzle.handle,
                'statement': puzzle.statementHTML,
                'type': puzzle.puzzleType,
                'author': puzzle.author,
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
