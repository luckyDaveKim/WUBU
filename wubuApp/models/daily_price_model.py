from django.db import models


class DailyPriceModel(models.Model):
    code = models.CharField(max_length=6, primary_key=True)
    date = models.DateField()
    open = models.BigIntegerField()
    high = models.BigIntegerField()
    low = models.BigIntegerField()
    close = models.BigIntegerField()
    diff = models.BigIntegerField()
    volume = models.BigIntegerField()

    class Meta:
        app_label = 'wubuApp'
        db_table = 'daily_price'
        unique_together = ['code', 'date']
