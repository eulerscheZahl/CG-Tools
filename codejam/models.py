from django.db import models

class Round(models.Model):
    name = models.CharField(max_length=40)
    order = models.IntegerField()

    @classmethod
    def create(cls, name):
        round = cls(name=name)
        round.save()
        return round


class Country(models.Model):
    name = models.CharField(max_length=50)

    @classmethod
    def create(cls, name):
        country = cls(name=name)
        country.save()
        return country


class User(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    @classmethod
    def create(cls, name, country):
        user = cls(name=name, country=country)
        user.save()
        return user


class RoundResult(models.Model):
    round = models.ForeignKey(Round, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    rank = models.IntegerField()
    points = models.IntegerField()
    time = models.IntegerField()

    unique_together = ('round', 'user')

    @classmethod
    def create(cls, round, user, rank, points, time):
        result = cls(round=round, user=user, rank=rank, points=points, time=time)
        result.save()
        return result
