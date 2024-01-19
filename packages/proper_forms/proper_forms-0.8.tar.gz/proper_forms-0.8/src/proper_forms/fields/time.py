from __future__ import annotations

from datetime import datetime, time

from .text import Text
from ..ftypes import type_time


__all__ = ("Time", )


class Time(Text):
    """A 12-hours or 24-hours time field, seconds optional.
    Examples: "5:03 AM", "11:00 PM", "4:20:16 PM".
    """

    input_type = "time"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.setdefault(
            "type", "Enter a time in a 12h or 24h format."
        )

    def prepare(self, object_value: datetime | time) -> list[str]:
        value = "{}:{:02d}".format(
            object_value.hour if object_value.hour <= 12 else object_value.hour - 12,
            object_value.minute
        )
        if object_value.second:
            value += ":{:02d}".format(object_value.second)
        value += object_value.strftime(" %p")
        return [value]

    def type(self, value: str) -> time | None:
        return type_time(value)
