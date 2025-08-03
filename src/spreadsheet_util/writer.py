import odswriter

from collections.abc import Iterable
from pathlib import Path


def _write_ods(filepath: Path, data: Iterable) -> None:
    with odswriter.writer(open(filepath, "wb")) as writer:
        writer.writerows(data)


def write(filepath: Path, data: Iterable) -> None:
    extension: str = filepath.suffix
    match extension:
        case ".ods":
            _write_ods(filepath, data)
        case _:
            raise ValueError(f"Unkown filetype {filepath}")
