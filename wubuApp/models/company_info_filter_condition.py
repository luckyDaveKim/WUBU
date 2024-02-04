from wubuApp.models.filter_condition import FilterCondition
from wubuApp.models.builder import Builder


class CompanyInfoFilterCondition(FilterCondition):
    def __init__(self):
        self.market_type = None

    def get_filter(self):
        filters = []

        if self.market_type:
            filters.append(('market_type', self.market_type))

        return filters

    @staticmethod
    def builder():
        return CompanyInfoFilterConditionBuilder()


class CompanyInfoFilterConditionBuilder(Builder):
    def __init__(self):
        self.object = CompanyInfoFilterCondition()

    def set_market_type(self, value):
        self.object.market_type = value
        return self

    def build(self):
        return self.object
