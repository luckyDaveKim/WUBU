from wubuApp.models.ruleStrategy.rule_bollinger_band_lower_bound import RuleBollingerBandLowerBound
from wubuApp.models.ruleStrategy.rule_bollinger_band_upper_bound import RuleBollingerBandUpperBound


class RuleExecutor:
    def __init__(self):
        value_name = 'close'
        self.rules = [
            RuleBollingerBandLowerBound(value_name, 10, 3),
            RuleBollingerBandUpperBound(value_name, 10, 2),
            RuleBollingerBandUpperBound(value_name, 10, 1),
            # RuleTrandChangeDownwardConvexPoint(value_name, 4),
        ]

    def execute(self, df) -> bool:
        for rule in self.rules:
            res = rule.execute(df)
            if not res.is_matched_rule():
                return False

        return True
