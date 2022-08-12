"""Module for validating command input with class descriptors."""


import re
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from wallaby.commands import Command


class OneOf:
    """A class descriptor that validates that the value is one of the given choices."""

    def __init__(
        self, *values: Any, preprocessor: Callable[[Any], Any] = lambda x: x
    ) -> None:
        self.options = values
        self.values = {}
        self.preprocessor = preprocessor

    def __set__(self, obj: "Command", value: Any) -> None:
        if (processed := self.preprocessor(value)) not in self.options:
            raise ValueError(f"{processed} is not one of {self.options}")
        self.values[obj] = processed

    def __get__(self, obj: "Command", _: Any) -> Any:
        return self.values[obj]

    def __delele__(self, obj: "Command") -> None:
        del self.values[obj]


class Pattern:
    """A class descriptor that validates that the value matches the given pattern."""

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern
        self.values = {}

    def __set__(self, obj: "Command", value: str) -> None:
        if not isinstance(value, str) or re.match(self.pattern, value) is None:
            raise ValueError(f"{value} does not match {self.pattern}")
        self.values[obj] = value

    def __get__(self, obj: "Command", _: Any) -> Any:
        return self.values[obj]

    def __delele__(self, obj: "Command") -> None:
        del self.values[obj]
