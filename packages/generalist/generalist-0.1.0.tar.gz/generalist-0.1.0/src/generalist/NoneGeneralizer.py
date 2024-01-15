from typing import Type, Any

from src.generalist.BaseGeneralizer import BaseGeneralizer


class NoneGeneralizer(BaseGeneralizer):
    def can_handle(self, _) -> bool:
        return True

    def inner_generalize(self, _) -> Any:
        return None

    def __str__(self):
        return "NoneGeneralizer()"
