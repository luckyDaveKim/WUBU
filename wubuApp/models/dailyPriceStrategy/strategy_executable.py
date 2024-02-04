from abc import ABC, abstractmethod


class StrategyExecutable(ABC):
    @abstractmethod
    def get_strategy_name(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self, df):
        raise NotImplementedError
