from abc import ABC, abstractmethod

from pandas import DataFrame

from wubuApp.models.ruleStrategy.condition_response import ConditionResponse


class ConditionExecutable(ABC):
    @abstractmethod
    def execute(self, df: DataFrame) -> ConditionResponse:
        raise NotImplementedError
