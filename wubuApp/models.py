from django.db import models


class CompanyInfo(models.Model):
    code = models.CharField(max_length=6, primary_key=True)
    company = models.CharField(max_length=40)
    market_type = models.CharField(max_length=20)
    last_update = models.DateField()

    class Meta:
        app_label = 'wubuApp'
        db_table = 'company_info'
