from rest_framework import serializers


class PlayerSerializer(serializers.Serializer):
    name = serializers.CharField()
    height = serializers.IntegerField()
    weight = serializers.FloatField()


class TeamSerializer(serializers.Serializer):
    goalie = PlayerSerializer()
    attackers = PlayerSerializer(many=True)
    defenders = PlayerSerializer(many=True)


class MatchSerializer(serializers.Serializer):
    home_team = TeamSerializer()
    away_team = TeamSerializer()
    highlights = serializers.ListField(child=serializers.CharField())
