from __future__ import annotations

import functools
import html
from typing import Iterable, Literal, Mapping, Union

from ._attrs import AttributeValue, serialize_attribute
from ._typing import Html, HtmlElement


class Element:
    """Lazily built HTML Element.

    An Element represents a Document Object Model (DOM) with optional
    attributes and children. Render the HTML to string by invoking the
    `__str__` method.
    """

    def __init__(self, tag: str) -> None:
        """Initialize element by providing a tag name, ie. "a", "div", etc."""
        self._tag = tag
        self._attrs: Mapping[str, AttributeValue] = {}
        self._children: Iterable[Child] = []

    def __call__(self, *children: Child, **attrs: AttributeValue) -> Element:
        """Add children and/or attributes to element.

        Provide attributes, children, or a combination of both:

        >>> import haitch as H
        >>> H.img(src="h.png", alt="Letter H")
        >>> H.h1("My heading")
        >>> H.h1(style="color: red;")("My heading")
        """
        if children:
            self._children = [*self._children, *children]

        if attrs:
            self._attrs = {**self._attrs, **attrs}

        return self

    @functools.cached_property
    def is_void(self) -> bool:
        """Check if element is considered a void element.

        https://developer.mozilla.org/en-US/docs/Glossary/Void_element
        """
        return self._tag in {
            "area",
            "base",
            "br",
            "col",
            "embed",
            "hr",
            "img",
            "input",
            "line",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        }

    def __str__(self) -> Html:
        """Renders the HTML element as a string."""
        return self._render()

    def _render(self) -> Html:
        attrs_ = "".join(serialize_attribute(k, v) for k, v in self._attrs.items())

        if self.is_void:
            return Html("<%(tag)s%(attrs)s/>" % {"tag": self._tag, "attrs": attrs_})

        children_ = "".join(self._render_child(child) for child in self._children)

        if self._tag == "fragment":
            return Html(children_)

        tmpl = "<%(tag)s%(attrs)s>%(children)s</%(tag)s>"

        if self._tag == "html":
            tmpl = "<!DOCTYPE html>" + tmpl

        html_str = tmpl % {"tag": self._tag, "attrs": attrs_, "children": children_}

        return Html(html_str)

    def _render_child(self, child: Child) -> str:
        if child is None or child is False:
            return ""

        if isinstance(child, str):
            return html.escape(child)

        if isinstance(child, HtmlElement):
            return child._render()

        if isinstance(child, Iterable):
            return "".join(str(nested_child) for nested_child in child)

        raise ValueError(f"Invalid child type: {type(child)}")


def fragment(*children: Child) -> Element:
    """Accepts only children as input and does not wrap its parent tag."""
    return Element("fragment")(*children)


EmptyChild = Literal[False, None]
"""An empty child type that may be passed to an element."""

ChildValue = Union[str, HtmlElement, EmptyChild]
"""An acceptable value for a child element."""

Child = Union[ChildValue, Iterable[ChildValue]]
"""An acceptable type to be passed to an element."""
