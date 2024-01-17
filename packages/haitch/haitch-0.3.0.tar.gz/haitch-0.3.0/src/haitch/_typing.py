from typing import NewType, Protocol, runtime_checkable

Html = NewType("Html", str)
"""A string representing rendered HTML."""


@runtime_checkable
class HtmlElement(Protocol):
    """An interface shared by all HTML elements."""

    def __str__(self) -> Html:
        ...

    def _render(self) -> Html:
        ...
