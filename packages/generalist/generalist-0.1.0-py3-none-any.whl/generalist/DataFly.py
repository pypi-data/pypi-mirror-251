from typing import List, Dict, Any

from src.generalist import BaseGeneralizer


class DataflyAlgo:
    def __init__(self, generalizers: Dict[str, BaseGeneralizer]):
        self._generalizers: Dict[str, BaseGeneralizer] = generalizers

    def anonymize(self, items: List) -> List[Any]:
        for item in items:
            for identifier in self._generalizers.keys():
                value = self._generalize(identifier, getattr(item, identifier))
                setattr(item, identifier, value)
        return items

    def _generalize(self, attribute, item) -> Any:
        if item is None:
            return None

        generalizer = self._generalizers.get(attribute)
        if generalizer.can_handle(item):
            return generalizer.generalize(item)

        raise ValueError("Cannot handle type: {}".format(type(item)))
