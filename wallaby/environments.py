from typing import Any, Optional, Type

import pydub

from wallaby.commands import Command
from wallaby.mixins import Component, Executable
from wallaby.validators import OneOf

DEFAULT_SCOPE = {cls.component_name: cls for cls in Command.__subclasses__()}


class BaseEnvironment:
    """The scope of the environment."""

    def __init__(self, parent: Optional["Environment"]) -> None:
        """Initialize the environment."""
        self.parent = parent
        self.scope: dict[str, Any] = {}
        self.body: list[Command | Environment] = []

    def __repr__(self) -> str:
        """Return a representation of the environment."""
        return f"{self.__class__.__name__}({self.scope})"

    def get(self, key: str) -> Any:
        """Lookup a command or variable in the environment."""
        if key in self:
            return self.scope[key]
        if self.parent is not None:
            return self.parent[key]
        return DEFAULT_SCOPE[key]

    def set(self, key: str, value: Any) -> None:
        """Set a variable or command in the environment."""
        env = self
        while env.parent is not None:
            env = env.parent
            if key in env.scope:
                env.scope[key] = value
                return
        self.scope[key] = value

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)

    def __contains__(self, key: str) -> bool:
        return key in self.scope

    @classmethod
    def delegate(cls, name: str) -> Type["Environment"]:
        """Delegate to the environment."""
        try:
            return {sub.component_name: sub for sub in Environment.__subclasses__()}[
                name
            ]
        except KeyError as err:
            raise NotImplementedError(f"No environment for {name}") from err


class Environment(BaseEnvironment, Command):
    """Represents an environment."""

    def __init__(self, parent: Optional["Environment"], *args: Any) -> None:
        """Initialize the parameters for the environment."""
        BaseEnvironment.__init__(self, parent)
        Command.__init__(self, *args)


class RootEnvironment(BaseEnvironment):
    """The first parent environment of a document."""

    def __init__(self) -> None:
        """Initialize the root environment."""
        BaseEnvironment.__init__(self, None)


class Stream(Environment, Component, component_name="stream"):
    """Represents a syncronous sound stream."""

    position: int = 0

    def compile(self) -> None:
        """Sets an empty sound stream."""
        self["__sound__"] = pydub.AudioSegment.empty()


class Definition(Environment, Component, component_name="define"):
    """Represents a repeatable musical sequence."""

    title: str

    def compile(self) -> None:
        """Create a command for the definition."""
        definition_body = self.body

        class DefinitionCommand(
            Command, Component, Executable, component_name=self.title
        ):
            """A command that plays a musical sequence."""

            repeat: int

            def __repr__(self) -> str:
                """Return a representation of the command."""
                return (
                    f"{self.__class__.__name__}({self.component_name}, {self.repeat})"
                )

            def execute(self, environment: "Environment") -> None:
                """Execute the command."""
                for _ in range(self.repeat):
                    for component in definition_body:
                        if isinstance(component, Environment):
                            component.compile()
                        else:
                            component.execute(environment)

        self.parent.scope[self.title] = DefinitionCommand


class Tempo(Environment, Component, component_name="tempo"):
    """An environment that has a set tempo for music it contains."""

    bpm: int

    def compile(self) -> None:
        """Execute the command."""
        self["tempo"] = self.bpm


class TimeSignature(Environment, Component, component_name="timesignature"):
    """An environment that has a set key signature for music it contains."""

    numerator: int
    denominator: int

    def compile(self) -> None:
        """Execute the command."""
        self["timesignature"] = self.numerator, self.denominator


class StaticDynamic(Environment, Component, component_name="dynamic"):
    """An environment that sets a static dynamic for music it contains."""

    dynamic: str

    def compile(self) -> None:
        """Execute the command."""
        self["dynamic"] = self.dynamic


class Instrument(Environment, Component, component_name="instrument"):
    """An environment that sets an instrument for music it contains."""

    instrument: str = OneOf(["piano", "organ", "guitar", "bass", "drums"])

    def compile(self) -> None:
        """Execute the command."""
        self["instrument"] = self.instrument


class Octave(Environment, Component, component_name="octave"):
    """An environment that sets a default octave for music it contains."""

    octave: int

    def compile(self) -> None:
        """Execute the command."""
        self["octave"] = self.octave
