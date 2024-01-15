from typing import Any

from src.generalist.BaseGeneralizer import BaseGeneralizer


class NumericGeneralizer(BaseGeneralizer):
    def __init__(self, step: float):
        self._step = step

    def can_handle(self, item: Any) -> bool:
        return isinstance(item, float) or isinstance(item, int)

    def inner_generalize(self, item: Any) -> Any:
        return round(item / self._step) * self._step

    def __str__(self):
        return "NumericGeneralizer(step={})".format(self._step)
