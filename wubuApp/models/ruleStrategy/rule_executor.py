from wubuApp.models.ruleStrategy.condition_bollinger_band_lower_bound import ConditionBollingerBandLowerBound
from wubuApp.models.ruleStrategy.condition_bollinger_band_upper_bound import ConditionBollingerBandUpperBound


class RuleExecutor:
    def __init__(self):
        value_name = 'close'
        self.conditions = [
            ConditionBollingerBandLowerBound(value_name, 10, 3),
            ConditionBollingerBandUpperBound(value_name, 10, 2),
            ConditionBollingerBandUpperBound(value_name, 10, 1),
            # RuleTrandChangeDownwardConvexPoint(value_name, 4),
        ]

    def execute(self, df) -> bool:
        for rule in self.conditions:
            res = rule.execute(df)
            if not res.is_matched_rule():
                return False

        return True
