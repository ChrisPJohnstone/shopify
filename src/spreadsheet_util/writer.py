from pathlib import Path

import odswriter


def _write_ods(filepath: Path, data: dict[str, list[tuple]]) -> None:
    with odswriter.writer(open(filepath, "wb")) as writer:
        for sheet_name, rows in data.items():
            sheet = writer.new_sheet(sheet_name)
            sheet.writerows(rows)


def write(filepath: Path, data: dict[str, list[tuple]]) -> None:
    extension: str = filepath.suffix
    match extension:
        case ".ods":
            _write_ods(filepath, data)
        case _:
            raise ValueError(f"Unkown filetype {filepath}")
