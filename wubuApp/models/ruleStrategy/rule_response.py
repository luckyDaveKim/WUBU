from pandas import DataFrame


class RuleResponse:
    def __init__(self, matched_rule: bool, df: DataFrame = None):
        self.matched_rule = matched_rule
        self.df = df

    def is_matched_rule(self):
        return self.matched_rule

    def get_df(self):
        return self.df

    @staticmethod
    def success(df: DataFrame):
        return RuleResponse(True, df)

    @staticmethod
    def successOnly():
        return RuleResponse(True)

    @staticmethod
    def failure(df: DataFrame):
        return RuleResponse(False, df)

    @staticmethod
    def failureOnly():
        return RuleResponse(False)
