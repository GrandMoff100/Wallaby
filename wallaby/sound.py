"""Module for compiling environments to sound."""
import pydub
from wallaby.environments import Stream, BaseEnvironment, Environment

from wallaby.parser import parse_text
from wallaby.const import FRAME_RATE


def execute(tree: BaseEnvironment) -> None:
    """Execute the whole AST."""
    for component in tree.body:
        if isinstance(component, Environment):
            execute(component)
        else:
            component.execute(tree)


def compile_text(text: str) -> pydub.AudioSegment:
    """Compile the text into a sound."""
    tree = parse_text(text)
    execute(tree)
    streams = [component for component in tree.body if isinstance(component, Stream)]
    main_audio = pydub.AudioSegment.silent(
        duration=max(len(stream.scope["__sound__"]) for stream in streams),
        frame_rate=FRAME_RATE,
    )
    for stream in streams:
        main_audio = main_audio.overlay(stream.scope["__sound__"], position=stream.position)
    return main_audio
