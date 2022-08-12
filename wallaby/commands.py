"""Module for document commands."""
from typing import TYPE_CHECKING, Any

import musicpy
import pydub

from wallaby.misc import counts_to_seconds
from wallaby.mixins import Component, Executable

from wallaby.validators import Pattern

if TYPE_CHECKING:
    from wallaby.environments import Environment


class Command:
    """Represents command calls."""

    def __init__(self, *args: Any) -> None:
        """Initialize the command."""
        for key, value in zip(self.__class__.__annotations__, args):
            setattr(self, key, value)


class Tag(Command, Component, Executable, component_name="tag"):
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

    note: str = Pattern(r"[A-G][#b]?[0-9]?")
    duration: int
    dynamic: str | None = None

    def __repr__(self) -> str:
        """Return a representation of the command."""
        return (
            f"{self.__class__.__name__}({self.note}, {self.duration}, {self.dynamic})"
        )

    def execute(self, environment: "Environment") -> None:
        """Execute the command."""
        dynamic = self.dynamic if self.dynamic is not None else environment["dynamic"]
        note = musicpy.note(self.note)
        print("Playing", note, dynamic)


class Rest(Command, Component, Executable, component_name="rest"):
    """A command that rests for a given duration."""

    counts: int

    def __repr__(self) -> str:
        """Return a representation of the command."""
        return f"{self.__class__.__name__}({self.counts})"

    def execute(self, environment: "Environment") -> None:
        """Append silence to the song."""
        environment["__sound__"] = environment["__sound__"].append(
            pydub.AudioSegment.silent(duration=counts_to_seconds(self.counts, environment["tempo"])),
            crossfade=0,
        )


class Print(Command, Component, Executable, component_name="print"):
    """A command that prints a message."""

    message: str

    def __repr__(self) -> str:
        """Return a representation of the command."""
        return f"{self.__class__.__name__}({self.message})"

    def execute(self, environment: "Environment") -> None:
        """Execute the command."""
        print(self.message)
