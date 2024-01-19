from __future__ import annotations

import re
import typing as t
from xml.sax.saxutils import quoteattr

from markupsafe import Markup


__all__ = ("get_html_attrs",)

rx_spaces = re.compile(r"\s+")


def get_html_attrs(attrs: dict | None = None, *, show_error: bool = False) -> str:
    """Generate HTML attributes from the provided attributes.

    - To provide consistent output, the attributes and properties are sorted by name
    and rendered like this: `<sorted attributes> + <sorted properties>`.
    - "classes" can be used intead of "class", to avoid clashes with the
    reserved word.
    - Also, all underscores are translated to regular dashes.
    - Set properties with a `True` value.

    >>> get_html_attrs({
    ...     "id": "text1",
    ...     "classes": "myclass",
    ...     "data_id": 1,
    ...     "checked": True,
    ... })
    'class="myclass" data-id="1" id="text1" checked'

    If `show_error` is true, the `error` attribute (or "error") is added
    to the classes, otherwise the attribute is ignored.

    """
    attrs = attrs or {}
    attrs_list = []
    props_list = []

    classes = attrs.pop("classes", "")
    error_classes = attrs.pop("error", "error")
    if show_error:
        classes = classes + " " + error_classes
    classes = classes.strip()

    classes_list = rx_spaces.split(classes) if classes else []
    if classes_list:
        attrs["class"] = " ".join(classes_list)

    for key, value in attrs.items():
        key = key.replace("_", "-")
        if value is True:
            props_list.append(key)
        elif value not in (False, None):
            value = quoteattr(str(value))
            attrs_list.append("{}={}".format(key, value))

    attrs_list.sort()
    props_list.sort()
    attrs_list.extend(props_list)
    return " ".join(attrs_list)


def render_error(error: str | None, *, tag: str = "div", **attrs: t.Any) -> Markup:
    if not error:
        return Markup("")

    attrs.setdefault("classes", "error")
    html_attrs = get_html_attrs(attrs, show_error=False)
    return Markup(f"<{tag} {html_attrs}>{error}</{tag}>")
