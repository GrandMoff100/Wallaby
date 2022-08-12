"""Module for miscellaneous utilities."""


def counts_to_seconds(counts: int, bpm: int) -> float:
    """Convert counts to seconds."""
    return counts * 60 / bpm
 