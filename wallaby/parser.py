"""Module for parsing text into Commands."""
import re
from typing import Any

from wallaby.converters import Converter
from wallaby.environments import Environment, RootEnvironment

ARGUMENT_PATTERN = r"\{(.*?)\}"
COMMAND_PATTERN = r"\\(?P<name>\w+)(?P<argument_values>(?:\{.*?\})*)"
ENVIRONMENT_PATTERN = (
    r"\\begin\{(?P<name>\w+)\}"
    r"(?P<argument_values>(?:\{.*?\})*)"
    r"(?P<body>(?:\\\w+(?:\{.*?\})*)*)"
    r"\\end{(?P=name)}"
)


def convert_arguments(cls: type, component: re.Match) -> list[Any]:
    """Convert arguments to specified types."""
    return [
        Converter.get_converter(arg_type).convert(arg)
        for arg, arg_type in zip(
            re.findall(
                ARGUMENT_PATTERN,
                component.group("argument_values"),
            ),
            cls.__annotations__.values(),
        )
    ]


def _parse_environment(component: re.Match, parent: Environment) -> Environment:
    env_type = Environment.delegate(component.group("name"))
    parent.body.append(
        new_env := _parse(
            component.group("body"),
            env_type(parent, *convert_arguments(env_type, component)),
        )
    )
    new_env.compile()


def _parse_command(component: re.Match, parent: Environment) -> None:
    command_cls = parent[component.group("name")]
    parent.body.append(command_cls(*convert_arguments(command_cls, component)))


def _parse(text: str, parent: Environment) -> Environment:
    while True:
        try:
            component, is_cmd = next_component(text)
        except StopIteration:
            break
        if is_cmd:
            _parse_command(component, parent)
        else:
            _parse_environment(component, parent)
        text = text.replace(component.group(0), "", 1)
    return parent


def next_component(text: str) -> tuple[re.Match | None, bool]:
    """Find the next component in the text."""
    next_environment = re.search(ENVIRONMENT_PATTERN, text)
    next_command = re.search(COMMAND_PATTERN, text)
    if next_environment is not None and next_command is not None:
        if next_environment.start() <= next_command.start():
            return next_environment, False
        return next_command, True
    if next_environment is not None:
        return next_environment, False
    if next_command:
        return next_command, True
    raise StopIteration()


def parse_text(text: str) -> RootEnvironment:
    """Compile text to a root environment."""
    return _parse(
        re.sub(
            r"\s*\n\s*",  # Remove newlines
            "",
            re.sub(r"#.*?\n(?<!\\)", "\n", text),  # Remove comments
        ),
        RootEnvironment(),
    )
