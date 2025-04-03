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
    highlights = serializers.ListField(child=serializers.CharField())
    home_team = TeamSerializer()
    away_team = TeamSerializer()
