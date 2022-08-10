from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from wallaby.environments import Environment


class Executable(Protocol):
    """A protocol for objects that can be executed."""

    def execute(self, environment: "Environment") -> None:
        """Execute the command."""
        raise NotImplementedError()


class Component:
    """Represents a named component."""

    component_name: str

    def __init_subclass__(cls, component_name: str) -> None:
        cls.component_name = component_name
