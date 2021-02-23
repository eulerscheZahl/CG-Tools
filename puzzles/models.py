import json

from django.db import models

class Puzzle(models.Model):
    handle = models.CharField(max_length=40)
    puzzle = models.TextField()
    comments = models.TextField()

    inputDescription = models.TextField(default="")
    outputDescription = models.TextField(default="")
    constraints = models.TextField(default="")
    title = models.TextField(default="", max_length=100, db_index=True)
    author = models.TextField(default="", max_length=100, db_index=True)
    testCases = models.TextField(default="")
    topics = models.TextField(default="", max_length=200, db_index=True)
    statement = models.TextField(default="")
    statementHTML = models.TextField(default="")
    commentText = models.TextField(default="")
    puzzleType = models.TextField(default="", max_length=40, db_index=True)

    def clean_html(self, html):
        open = html.count('<div')
        close = html.count('</div')
        return '<div>' * max(0, close-open) + html + '</div>' * max(0, open-close)

    def extract_fields(self):
        data = json.loads(self.puzzle)
        last_version = data['lastVersion']['data']

        self.author = data['nickname'] if 'nickname' in data else 'unknown'
        self.puzzleType = data['type']
        self.title = data['title']
        if 'inputDescription' in last_version: self.inputDescription = last_version['inputDescription']
        if 'outputDescription' in last_version: self.outputDescription = last_version['outputDescription']
        if 'constraints' in last_version: self.constraints = last_version['constraints']
        if 'testCases' in last_version:
            self.testCases = ''
            for test in last_version['testCases']:
                self.testCases += str(test['title']) + '\n' + str(test['testIn']) + '\n' + str(test['testOut']) + '\n'
        self.topics = ''
        if 'topics' in last_version:
            for tag in last_version['topics']:
                for language in tag['labelMap'].keys():
                    if language == '2': self.topics += tag['labelMap'][language] + '\n'
        if self.comments != '':
            for comment in json.loads(self.comments): self.commentText += comment['content'] + '\n'

        if 'statement' in last_version: self.statement = last_version['statement']
        if 'statementHTML' in data['lastVersion']: # classic puzzle
            self.statementHTML = data['lastVersion']['statementHTML']
        elif 'statement' in data['lastVersion']['data']: # classic puzzle
            self.statementHTML = data['lastVersion']['data']['statement']
        else: # interactive
            self.statementHTML = data['lastVersion']['data']['levelParams']
            key = sorted(list(self.statementHTML.keys()))[-1]
            self.statementHTML = self.statementHTML[key]['statements']['2']
        self.statementHTML = self.clean_html(self.statementHTML)
        if self.statement == '': self.statement = self.statementHTML

    def extract_fields_save(self):
        self.extract_fields()
        self.save()

    def save(self, *args, **kwargs):
        self.extract_fields()
        super(Puzzle, self).save(*args, **kwargs)
