from django.db import models

class Puzzle(models.Model):
    handle = models.CharField(max_length=40)
    puzzle = models.TextField()
    comments = models.TextField()
