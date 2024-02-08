from abc import ABC, abstractmethod

from pandas import DataFrame

from wubuApp.models.ruleStrategy.rule_response import RuleResponse


class RuleExecutable(ABC):
    @abstractmethod
    def execute(self, df: DataFrame) -> RuleResponse:
        raise NotImplementedError
