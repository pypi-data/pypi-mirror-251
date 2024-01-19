from __future__ import annotations

from .text import Text
from ..ftypes import type_hex_color


__all__ = ("HexColor",)


class HexColor(Text):
    """Accepts a color in hex, rgb, or rgba color and normalize it to a hex value
    of 6 digits or 6 digits plus one for alpha.

    Examples:

    - "#f2e" -> "#ff22ee"
    - "rgb(255, 0, 255)" -> "#ff00ff"
    - "rgb(221, 96, 89)" -> "#dd6059"
    - "rgba(221, 96, 89, 0.3)" -> "#dd60594c"
    """

    input_type = "color"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.setdefault(
            "type", "Enter color in #hex, rgb() or rgba() format."
        )

    def type(self, value: str) -> str | None:
        return type_hex_color(value)
