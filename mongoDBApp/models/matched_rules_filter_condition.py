from wubuApp.models.builder import Builder
from wubuApp.models.filter_condition import FilterCondition


class MatchedRulesFilterCondition(FilterCondition):
    def __init__(self):
        self.code = None
        self.analysis_date = None
        self.start_analysis_date = None
        self.end_analysis_date = None

    def get_filter(self):
        filters = []

        if not self.code \
                and not self.analysis_date \
                and not self.start_analysis_date and not self.end_analysis_date:
            raise ValueError("code 와 analysis_date 중 하나는 정의되어야 합니다!")

        if self.code:
            filters.append(('code', self.code))

        # if self.analysis_date or self.start_analysis_date or self.end_analysis_date:
        #     if self.analysis_date:
        #         filters.append(('analysis_date', self.analysis_date))
        #     else:
        #         if self.start_analysis_date and self.end_analysis_date:
        #             filters.append(
        #                 (
        #                     'analysis_date__range',
        #                     [self.start_analysis_date, self.end_analysis_date]
        #                 )
        #             )
        #         elif self.start_analysis_date:
        #             filters.append(
        #                 ('analysis_date__gte', self.start_analysis_date)
        #             )
        #         elif self.end_analysis_date:
        #             filters.append(
        #                 ('analysis_date__lte', self.end_analysis_date)
        #             )

        return filters

    @staticmethod
    def builder():
        return MatchedRulesFilterConditionBuilder()


class MatchedRulesFilterConditionBuilder(Builder):
    def __init__(self):
        self.object = MatchedRulesFilterCondition()

    def set_code(self, value):
        self.object.code = value
        return self

    def set_analysis_date(self, value):
        self.object.analysis_date = value
        return self

    def set_start_analysis_date(self, value):
        self.object.start_analysis_date = value
        return self

    def set_end_analysis_date(self, value):
        self.object.end_analysis_date = value
        return self

    def build(self):
        return self.object
