from pandas import DataFrame

from wubuApp.models.ruleStrategy.condition_response import ConditionResponse


class TrandChangeDetect:
    """
    Parameters:
    - value_name (str): 비교값
    - downward_convex (bool): 아래로 볼록한 변곡점인지 여부 (기본값: True, 즉, 아래로 볼록한 변곡점)
    """

    def __init__(self,
                 value_name: str,
                 downward_convex: bool = True):
        self.value_name = value_name
        self.downward_convex = downward_convex

    """
    Parameters:
    - df (DataFrame): 데이터프레임
    - previous_nth (int): 변곡점인지 확인할, n번째 전 df 값
    """

    def check(self, df: DataFrame, previous_nth: int) -> ConditionResponse:
        if len(df) < previous_nth or previous_nth <= 0:
            raise ValueError(f"DataFrame의 길이 {len(df)} 보다 작고 0보다 큰 previous_nth: {previous_nth} 값을 사용해주세요.")

        if previous_nth == len(df) or previous_nth == 1:
            raise ValueError("양 끝 데이터는 변곡점을 확인할 수 없습니다.")

        prev_row = df.iloc[-previous_nth - 1]
        row = df.iloc[-previous_nth]
        post_row = df.iloc[-previous_nth + 1]

        prev_value = prev_row[self.value_name]
        target_value = row[self.value_name]
        post_value = post_row[self.value_name]

        if self.downward_convex:
            # 아래로 볼록한 변곡점인지 판단
            matched_rule = target_value < prev_value and target_value < post_value
            print(f'Do downwardConvex check res: {matched_rule}')
        else:
            # 위로 볼록한 변곡점인지 판단
            matched_rule = target_value > prev_value and target_value > post_value
            print(f'Do upwardConvex check res: {matched_rule}')

        return ConditionResponse.success(df) if matched_rule else ConditionResponse.failure(df)
