from pandas import DataFrame

from wubuApp.models.ruleStrategy.rule_executable import RuleExecutable
from wubuApp.models.ruleStrategy.rule_response import RuleResponse
from wubuApp.models.ruleStrategy.trand_change_detect import TrandChangeDetect


class RuleTrandChangeDownwardConvexPoint(RuleExecutable):
    """

    Parameters:
    - value_name (str): 아래로 볼락한 변곡점인지 확인할 비교값
    - previous_nth (int): 변곡점인지 확인할, n번째 전 df 값
    """

    def __init__(self, value_name: str, previous_nth: int):
        self.previous_nth = previous_nth
        self.trand_change_detect = TrandChangeDetect(value_name, True)

    def execute(self, df: DataFrame) -> RuleResponse:
        return self.trand_change_detect.check(df, self.previous_nth)
