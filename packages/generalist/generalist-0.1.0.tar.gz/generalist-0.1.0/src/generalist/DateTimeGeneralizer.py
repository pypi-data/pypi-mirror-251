import datetime
from typing import Any

from src.generalist.BaseGeneralizer import BaseGeneralizer


class DateTimeGeneralizer(BaseGeneralizer):
    def can_handle(self, item: Any) -> bool:
        return isinstance(item, datetime.datetime)

    def inner_generalize(self, item: Any) -> Any:
        dt: datetime = item
        if dt.time() > datetime.time.min:
            return datetime.datetime.combine(dt.date(), datetime.time.min)
        elif dt.day.real > 1:
            return dt.replace(dt.year, dt.month, 1)
        else:
            return dt.replace(dt.year, 1, 1)

    def __str__(self):
        return "DateTimeGeneralizer()"
