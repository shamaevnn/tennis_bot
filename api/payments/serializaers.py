from rest_framework import serializers

from api.players.serializers import GetPlayerSerializer
from base.models import Payment


class GetPaymentSerializer(serializers.ModelSerializer):
    player = GetPlayerSerializer()

    class Meta:
        model = Payment
        fields = "__all__"
