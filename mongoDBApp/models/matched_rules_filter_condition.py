from wubuApp.models.builder import Builder
from wubuApp.models.filter_condition import FilterCondition


class MatchedRulesFilterCondition(FilterCondition):
    def __init__(self):
        self.analysis_date = None

    def get_filter(self):
        filters = []

        if self.analysis_date:
            filters.append(('analysis_date', self.analysis_date))

        return filters

    @staticmethod
    def builder():
        return MatchedRulesFilterConditionBuilder()


class MatchedRulesFilterConditionBuilder(Builder):
    def __init__(self):
        self.object = MatchedRulesFilterCondition()

    def set_analysis_date(self, value):
        self.object.analysis_date = value
        return self

    def build(self):
        return self.object
