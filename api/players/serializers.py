from rest_framework import serializers

from base.models import Player


class GetPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        exclude = ("parent",)
