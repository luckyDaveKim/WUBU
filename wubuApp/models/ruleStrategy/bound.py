from pandas import DataFrame, Series

from wubuApp.models.ruleStrategy.condition_response import ConditionResponse


class Bound:
    """

    Parameters:
    - value_name (str): 비교값
    - upper_value_name (str): 상위 값
    - lower_value_name (str): 하위 값
    - n_percent (float): 상/하위 n% 확인을 위한 (0~100)값
    - upper_bound (bool): 상한 범위 여부 (기본값: True, 즉, 상위 범위)
    """

    def __init__(self,
                 value_name: str,
                 upper_value_name: str,
                 lower_value_name: str,
                 n_percent: float,
                 upper_bound: bool = True):
        self.value_name = value_name
        self.upper_value_name = upper_value_name
        self.lower_value_name = lower_value_name
        self.n_percent = n_percent
        self.upper_bound = upper_bound

        if self.n_percent < 0 or self.n_percent > 100:
            raise ValueError(f"n_percent: {n_percent} 값은 0~100 사이의 값 이여야 합니다!")

    def check_bound_nth_previous(self, df: DataFrame, previous_nth: int) -> ConditionResponse:
        if len(df) < previous_nth or previous_nth <= 0:
            raise ValueError(f"DataFrame의 길이 {len(df)} 보다 작고 0보다 큰 previous_nth: {previous_nth} 값을 사용해주세요.")

        row = df.iloc[-previous_nth]
        matched_rule = self.check_bound(row).is_matched_rule()
        return ConditionResponse.success(df) if matched_rule else ConditionResponse.failure(df)

    def check_bound(self, row: Series) -> ConditionResponse:
        if row.empty:
            raise ValueError("row 값이 존재하지 않습니다!")

        value = row[self.value_name]
        upper = row[self.upper_value_name]
        lower = row[self.lower_value_name]
        if not (value or upper or lower):
            raise ValueError(f"value: {value}, upper: {upper}, lower: {lower} 값이 존재하지 않습니다!")

        threshold_value = (upper - lower) * (self.n_percent / 100) + lower

        if self.upper_bound:
            print(f'Do upperBound res: {threshold_value <= value}, threshold_value: {threshold_value}, value: {value}')
            # upper_bound 일 때, value 가 상위 n% 이상이면 성공, 미만이면 실패
            return ConditionResponse.successOnly() if threshold_value <= value else ConditionResponse.failureOnly()
        else:
            print(f'Do lowerBound res: {value <= threshold_value}, threshold_value: {threshold_value}, value: {value}')
            # lower_bound 일 때, value 가 하위 n% 이하면 성공, 초과면 실패
            return ConditionResponse.successOnly() if value <= threshold_value else ConditionResponse.failureOnly()
