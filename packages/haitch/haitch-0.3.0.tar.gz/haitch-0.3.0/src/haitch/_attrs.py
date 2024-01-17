import html
from typing import Union

AttributeValue = Union[str, bool]
"""An acceptable value type to be passed to an attribute."""


def serialize_attribute(key: str, value: AttributeValue) -> str:
    """Convert a key value pair into a valid HTML attribute."""
    key_ = key.rstrip("_").replace("_", "-")

    if isinstance(value, bool):
        return " %(key)s" % {"key": key_} if value else ""

    if isinstance(value, str):
        value_ = html.escape(value)
        return ' %(key)s="%(value)s"' % {"key": key_, "value": value_}

    raise ValueError(f"Attribute value must be `str` or `bool`, not {type(value)}")
