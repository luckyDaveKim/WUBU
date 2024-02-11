from pandas import DataFrame


class ConditionResponse:
    def __init__(self, matched_rule: bool, df: DataFrame = None):
        self.matched_rule = matched_rule
        self.df = df

    def is_matched_rule(self):
        return self.matched_rule

    def get_df(self):
        return self.df

    @staticmethod
    def success(df: DataFrame):
        return ConditionResponse(True, df)

    @staticmethod
    def successOnly():
        return ConditionResponse(True)

    @staticmethod
    def failure(df: DataFrame):
        return ConditionResponse(False, df)

    @staticmethod
    def failureOnly():
        return ConditionResponse(False)
