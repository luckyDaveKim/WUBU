from pandas import DataFrame

from wubuApp.models.ruleStrategy.bound import Bound
from wubuApp.models.ruleStrategy.rule_executable import RuleExecutable
from wubuApp.models.ruleStrategy.rule_response import RuleResponse


class RuleBollingerBandLowerBound(RuleExecutable):
    """

    Parameters:
    - value_name (str): 볼린저 밴드 하위 n% 에 속하는지 확인할 비교값
    - n_percent (float): 볼린저 밴드 내에서 하위 n% 에 속하는지 확인을 위한 (0~100)값
    - previous_nth (int): n번째 전 df 값
    """

    def __init__(self, value_name: str, n_percent: float, previous_nth: int):
        upper_value_name = 'bollingerBandUpper'
        lower_value_name = 'bollingerBandLower'
        self.previous_nth = previous_nth
        self.bound = Bound(value_name, upper_value_name, lower_value_name, n_percent, False)

    def execute(self, df: DataFrame) -> RuleResponse:
        return self.bound.check_bound_nth_previous(df, self.previous_nth)
