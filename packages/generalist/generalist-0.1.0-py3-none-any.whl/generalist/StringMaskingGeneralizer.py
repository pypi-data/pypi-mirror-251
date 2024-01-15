from typing import Any

from src.generalist.BaseGeneralizer import BaseGeneralizer


class StringMaskingGeneralizer(BaseGeneralizer):
    def __init__(self, mask: str, start: int = 0, length: int = 10):
        if start > length:
            length = start
        self._length = length
        self._start = start
        self._mask = mask

    def can_handle(self, item: Any) -> bool:
        return isinstance(item, str)

    def inner_generalize(self, item: Any) -> Any:
        prefix = str(item)[:self._start]
        suffix = (self._mask * self._length)[:self._length - self._start]
        return prefix + suffix

    def __str__(self):
        return "StringMaskingGeneralizer(mask={})".format(self._mask)
