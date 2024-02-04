from datetime import datetime
from rest_framework import serializers

from wubuApp.models import DailyPriceModel


class DailyPriceSerializer(serializers.ModelSerializer):
    date_timestamp = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_date_timestamp(self, obj):
        datetime_object = datetime.combine(obj.date, datetime.min.time())
        return int(datetime_object.timestamp() * 1_000)

    def get_price(self, obj):
        return [obj.open, obj.high, obj.low, obj.close]

    class Meta:
        model = DailyPriceModel
        fields = ['date_timestamp', 'price']
