from django.db import models
from django.template.defaulttags import regroup


class Leaderboard(models.Model):
    game = models.TextField()
    botReplays = models.TextField()
    replayGroups = models.TextField()

    @staticmethod
    def updateEntry(game, botReplays, replayGroups):
        leaderboard = Leaderboard.objects.filter(game=game).first()
        if leaderboard == None:
            leaderboard = Leaderboard(
                game=game, botReplays=botReplays, replayGroups=replayGroups)
            leaderboard.save()
        else:
            leaderboard.botReplays = botReplays
            leaderboard.replayGroups = replayGroups
            leaderboard.save()
