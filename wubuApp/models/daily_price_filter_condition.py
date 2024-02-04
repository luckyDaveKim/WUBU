from datetime import datetime

from wubuApp.models.filter_condition import FilterCondition
from wubuApp.models.builder import Builder

DATE_FORMAT = '%Y-%m-%d'


class DailyPriceFilterCondition(FilterCondition):
    def __init__(self):
        self.code = None
        self.start_date = None
        self.end_date = None

    def get_filter(self):
        filters = []

        if self.code:
            filters.append(('code', self.code))

        if self.start_date or self.end_date:
            try:
                if self.start_date and self.end_date:
                    filters.append(
                        (
                            'date__range',
                            [datetime.strptime(self.start_date, DATE_FORMAT),
                             datetime.strptime(self.end_date, DATE_FORMAT)]
                        )
                    )
                elif self.start_date:
                    filters.append(
                        ('date__gte', datetime.strptime(self.start_date, DATE_FORMAT))
                    )
                elif self.end_date:
                    filters.append(
                        ('date__lte', datetime.strptime(self.end_date, DATE_FORMAT))
                    )
            except Exception as e:
                print('start_date, end_date 파싱 오류!!!', e)

        return filters

    @staticmethod
    def builder():
        return DailyPriceFilterConditionBuilder()


class DailyPriceFilterConditionBuilder(Builder):
    def __init__(self):
        self.object = DailyPriceFilterCondition()

    def set_code(self, value):
        self.object.code = value
        return self

    def set_start_date(self, value):
        self.object.start_date = value
        return self

    def set_end_date(self, value):
        self.object.end_date = value
        return self

    def build(self):
        return self.object
