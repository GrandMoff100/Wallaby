"""Module for document commands."""
from typing import TYPE_CHECKING, Any

import pydub

from wallaby.mixins import Component, Executable

if TYPE_CHECKING:
    from wallaby.environments import Environment

from wallaby.const import SIXTY_SECONDS


class Command:
    """Represents command calls."""

    def __init__(self, *args: Any) -> None:
        """Initialize the command."""
        for key, value in zip(self.__class__.__annotations__, args):
            setattr(self, key, value)


class Tag(Command, Component, Executable, component_name="author"):
    """A command that set a song metadata tag."""

    tag_name: str
    tag_value: str

    def execute(self, environment: "Environment") -> None:
        """Execute the command."""
        pair = {self.tag_name: self.tag_value}
        if "tags" not in environment.scope:
            environment.scope["tags"] = pair
        else:
            environment.scope["tags"].update(pair)

    def __repr__(self) -> str:
        """Return a representation of the command."""
        return f"{self.__class__.__name__}({self.tag_name}, {self.tag_value})"


class Play(Command, Component, Executable, component_name="play"):
    """A command that plays a note."""

    note: str
    duration: int
    dynamic: str | None = None

    def __repr__(self) -> str:
        """Return a representation of the command."""
        return (
            f"{self.__class__.__name__}({self.note}, {self.duration}, {self.dynamic})"
        )

    def execute(self, environment: "Environment") -> None:
        """Execute the command."""
        if self.dynamic is not None:
            dynamic = self.dynamic
        else:
            dynamic = environment["dynamic"]
        print("Playing", self.note, self.duration, dynamic)


class Rest(Command, Component, Executable, component_name="rest"):
    """A command that rests for a given duration."""

    counts: int

    def __repr__(self) -> str:
        """Return a representation of the command."""
        return f"{self.__class__.__name__}({self.counts})"

    def execute(self, environment: "Environment") -> None:
        """Execute the command."""
        tempo = environment["tempo"]
        environment["__sound__"] = environment["__sound__"].append(
            pydub.AudioSegment.silent(duration=self.counts * SIXTY_SECONDS / tempo)
        )
