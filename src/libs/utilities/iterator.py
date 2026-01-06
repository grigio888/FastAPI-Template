"""
Utilities - Iterator.
"""

from collections.abc import Iterator
from csv import DictReader
from pathlib import Path


def iter_items(file_path: str | Path) -> Iterator[dict[str, str]]:
    """
    Iterate over items from a CSV file.
    """

    path = Path(file_path)

    with path.open(newline="", encoding="utf-8") as handle:
        reader = DictReader(handle)
        yield from reader
