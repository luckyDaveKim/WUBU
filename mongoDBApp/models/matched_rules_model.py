from mongoengine import Document, StringField, DateField, DictField


class MatchedRulesModel(Document):
    code = StringField(max_length=6)
    analysis_date = DateField()
    rules = DictField()

    class Meta:
        app_label = 'mongoDBApp'
        db_table = 'matched_rules'
        unique_together = ['code', 'analysis_date']
