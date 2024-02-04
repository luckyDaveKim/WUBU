from abc import ABC, abstractmethod


class FilterCondition(ABC):
    @abstractmethod
    def get_filter(self):
        pass
