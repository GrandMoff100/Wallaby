"""Module for compiling environments to sound."""
import pydub

from wallaby.const import FRAME_RATE
from wallaby.environments import (BaseEnvironment, Environment,
                                  RootEnvironment, Stream)
from wallaby.mixins import Component
from wallaby.parser import parse_text


class Soundfont(Environment, Component, component_name="soundfont"):
    """An environment that tells notes to render with a different instrument."""

    soundfont: str

    def compile(self) -> None:
        """Execute the command."""
        self.scope["soundfont"] = self.soundfont


def execute(tree: BaseEnvironment) -> None:
    """Execute the whole AST."""
    for component in tree.body:
        if isinstance(component, Environment):
            execute(component)
        else:
            component.execute(tree)


def compile_text(text: str) -> tuple[pydub.AudioSegment, RootEnvironment]:
    """Compile the text into a sound."""
    tree = parse_text(text)
    execute(tree)
    streams = [component for component in tree.body if isinstance(component, Stream)]
    main_audio = pydub.AudioSegment.silent(
        duration=max(len(stream["__sound__"]) for stream in streams),
        frame_rate=FRAME_RATE,
    )
    for stream in streams:
        main_audio = main_audio.overlay(stream["__sound__"], position=stream.position)
    return main_audio, tree
