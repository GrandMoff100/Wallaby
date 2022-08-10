from typing import Any, Optional, Type

from wallaby.commands import Command
from wallaby.mixins import Component, Executable

DEFAULT_SCOPE = {cls.component_name: cls for cls in Command.__subclasses__()}


class BaseEnvironment:
    """The scope of the environment."""

    def __init__(self, parent: Optional["Environment"]) -> None:
        """Initialize the environment."""
        self.parent = parent
        self.scope = {}
        self.body = []

    def __repr__(self) -> str:
        """Return a representation of the environment."""
        return f"{self.__class__.__name__}({self.scope})"

    def lookup(self, key: str) -> Type[Command]:
        """Lookup a command in the environment."""
        if key in self.scope:
            return self.scope[key]
        if self.parent is not None:
            return self.parent.lookup(key)
        return DEFAULT_SCOPE[key]

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


class Music(BaseEnvironment):
    """An environment where music is played."""

    def execute(self) -> None:
        """Execute the environment."""
        for component in self.body:
            if isinstance(component, Environment):
                component.execute()
            else:
                component.execute(self)


class RootEnvironment(BaseEnvironment):
    """The first parent environment of a document."""

    def __init__(self) -> None:
        """Initialize the root environment."""
        BaseEnvironment.__init__(self, None)


class Stream(Environment, Component, component_name="stream"):
    """Represents a syncronous sound stream."""

    def execute(self) -> None:
        """Execute the environment."""


class Definition(Environment, Component, component_name="define"):
    """Represents a repeatable musical sequence."""

    title: str

    def execute(self) -> None:
        """Create a command for the definition."""
        definition_body = self.body

        class DefinitionCommand(
            Command, Component, Executable, component_name=self.title
        ):
            """A command that plays a musical sequence."""

            repeat: int

            def execute(self, environment: "Environment") -> None:
                """Execute the command."""
                for _ in range(self.repeat):
                    for component in definition_body:
                        if isinstance(component, Environment):
                            component.execute()
                        else:
                            component.execute(environment)

        self.parent.scope[self.title] = DefinitionCommand


class Tempo(Environment, Component, component_name="tempo"):
    """An environment that has a set tempo for music it contains."""

    bpm: int

    def execute(self) -> None:
        """Execute the command."""
        self.scope["tempo"] = self.bpm


class TimeSignature(Environment, Component, component_name="timesignature"):
    """An environment that has a set key signature for music it contains."""

    numerator: int
    denominator: int

    def execute(self) -> None:
        """Execute the command."""
        self.scope["timesignature"] = f"{self.numerator}/{self.denominator}"


class StaticDynamic(Environment, Component, component_name="dynamic"):
    """A command that sets a static dynamic for music it contains."""

    dynamic: str

    def execute(self) -> None:
        """Execute the command."""
        self.scope["dynamic"] = self.dynamic
