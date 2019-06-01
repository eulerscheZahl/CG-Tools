from .models import Round, Country, User, RoundResult
from rest_framework import serializers


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = ['name', 'order']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'country']

    def get_fields(self):
        fields = super(UserSerializer, self).get_fields()
        fields['country'] = CountrySerializer()
        return fields


class RoundResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RoundResult
        fields = ['round', 'user', 'rank', 'points', 'time']

    def get_fields(self):
        fields = super(RoundResultSerializer, self).get_fields()
        fields['user'] = UserSerializer()
        fields['round'] = RoundSerializer()
        return fields
