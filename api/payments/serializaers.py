from rest_framework import serializers

from api.players.serializers import GetPlayerSerializer
from base.common_for_bots.static_text import from_digit_to_month
from base.models import Payment


class GetPaymentSerializer(serializers.ModelSerializer):
    player = GetPlayerSerializer()
    rus_month = serializers.SerializerMethodField()
    full_digit_year = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = "__all__"

    def get_rus_month(self, obj: Payment):
        return from_digit_to_month[int(obj.month)]

    def get_full_digit_year(self, obj: Payment):
        return 2020 + int(obj.year)
