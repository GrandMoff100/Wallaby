"""Module for parsing text into python data structures."""

import datetime
from types import UnionType
from typing import Any, Type


class Converter:
    """Converts a string into a python object."""

    def __init_subclass__(cls, data_type: type) -> None:
        cls.data_type = data_type

    @classmethod
    def get_converter(cls, data_type: Type[Any]) -> Type["Converter"]:
        """Return a converter for the given type."""
        if isinstance(data_type, UnionType):
            return Converter.get_converter(
                data_type.__args__[0]
            ) or Converter.get_converter(data_type.__args__[1])
        for subcls in cls.__subclasses__():
            if subcls.data_type == data_type:
                return subcls

    @classmethod
    def convert(cls, value: str) -> Any:
        """Convert a string into a python object."""
        raise NotImplementedError()


class String(Converter, data_type=str):
    """Converts a string into a string."""

    @classmethod
    def convert(cls, value: str) -> str:
        return value


class Int(Converter, data_type=int):
    """Converts a string into an integer."""

    @classmethod
    def convert(cls, value: str) -> int:
        return int(value)


class Float(Converter, data_type=float):
    """Converts a string into a float."""

    @classmethod
    def convert(cls, value: str) -> float:
        return float(value)


class DateTime(Converter, data_type=datetime.datetime):
    """Converts a string into a datetime."""

    @classmethod
    def convert(cls, value: str) -> datetime.datetime:
        return datetime.datetime.fromisoformat(value)


class Bool(Converter, data_type=bool):
    """Converts a string into a boolean."""

    @classmethod
    def convert(cls, value: str) -> bool:
        return {"true": True, "false": False}[value.lower()]
