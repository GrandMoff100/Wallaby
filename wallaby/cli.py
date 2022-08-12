"""Module for command line interfacing."""

import io
import logging

import click

from wallaby.sound import compile_text

LOGGER = logging.getLogger(__name__)


def set_log_level(_: click.Context, __: click.Parameter, value: str) -> None:
    """Set the log level."""
    logging.basicConfig(level=value)


@click.command()
@click.argument("file", type=click.File("r"))
@click.argument("output", type=click.Path(exists=False))
@click.option("--log-level", default="INFO", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]), callback=set_log_level, expose_value=False)
@click.option("--audio-format", "-f", default="mp3", help="Audio file format to use.")
@click.option("--bitrate", "-b", default=320, type=int, help="Audio bitrate to use. (In kilobytes)")
@click.option(
    "--cover",
    "-c",
    type=click.Path(readable=True),
    help="Cover image to use.",
    default=None,
)
def main(
    file: io.TextIOWrapper,
    output: str,
    audio_format: str,
    bitrate: int,
    cover: str | None = None,
) -> None:
    """Compile a text file to an audio output file."""
    LOGGER.info("Compiling %s to %s", file.name, output)
    audio, tree = compile_text(file.read())

    LOGGER.info("Writing %s", output)
    params = {"format": audio_format, "bitrate": f"{bitrate}k"}
    if cover is not None:
        params["cover"] = cover
    if "tags" in tree:
        params["tags"] = tree["tags"]
    audio.export(output, **params)

    LOGGER.info("Compiled successfully")
