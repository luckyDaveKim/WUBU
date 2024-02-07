from rest_framework import serializers

from wubuApp.models import DailyPriceModel


class DailyPriceSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        return [obj.open, obj.high, obj.low, obj.close]

    class Meta:
        model = DailyPriceModel
        fields = ['price']
