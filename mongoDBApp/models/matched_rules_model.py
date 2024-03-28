from djongo import models


class MatchedRulesModel(models.Model):
    code = models.CharField(max_length=6, primary_key=True)
    # analysis_date = models.DateTimeField()
    rules = models.TextField()
    # rules = models.JSONField()

    class Meta:
        app_label = 'mongoDBApp'
        db_table = 'matched_rules'
        # unique_together = ['code', 'rules']
        # unique_together = ['code', 'analysis_date']
