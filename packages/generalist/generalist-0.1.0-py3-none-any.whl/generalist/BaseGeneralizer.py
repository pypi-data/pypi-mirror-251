from typing import Any
from abc import ABC, abstractmethod


class BaseGeneralizer(ABC):

    @abstractmethod
    def can_handle(self, item: Any) -> bool:
        pass

    def generalize(self, item: Any):
        if item is None:
            return None

        return self.inner_generalize(item)

    @abstractmethod
    def inner_generalize(self, item: Any) -> Any:
        pass
