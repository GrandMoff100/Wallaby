"""Module for document commands."""
from typing import TYPE_CHECKING, Any

from wallaby.mixins import Component, Executable

if TYPE_CHECKING:
    from wallaby.environments import Environment


class Command:
    """Represents command calls."""

    def __init__(self, *args: Any) -> None:
        """Initialize the command."""
        for key, value in zip(self.__class__.__annotations__, args):
            setattr(self, key, value)


class Author(Command, Component, Executable, component_name="author"):
    """A command that sets the song author."""

    author_name: str

    def execute(self, environment: "Environment") -> None:
        """Execute the command."""
        environment["author"] = self.author_name

    def __repr__(self) -> str:
        """Return a representation of the command."""
        return f"{self.__class__.__name__}({self.author_name})"

class Title(Command, Component, Executable, component_name="title"):
    """A command that sets the song title."""

    title: str

    def execute(self, environment: "Environment") -> None:
        """Execute the command."""
        environment["title"] = self.title

    def __repr__(self) -> str:
        """Return a representation of the command."""
        return f"{self.__class__.__name__}({self.title})"

class Play(Command, Component, Executable, component_name="play"):
    """A command that plays a note."""

    note: str
    duration: int
    dynamic: str | None = None

    def __repr__(self) -> str:
        """Return a representation of the command."""
        return f"{self.__class__.__name__}({self.note}, {self.duration}, {self.dynamic})"

    def execute(self, environment: "Environment") -> None:
        """Execute the command."""
        if self.dynamic is not None:
            dynamic = self.dynamic
        else:
            dynamic = environment.lookup("dynamic")
        print("Playing", self.note, self.duration, dynamic)
