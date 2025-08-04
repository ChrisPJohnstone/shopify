#!/usr/bin/env python3
from __future__ import unicode_literals
from collections.abc import Iterable
from pathlib import Path
from typing import Any
import sys

import uno

PROJECT_DIR: Path = Path("PATH_PLACEHOLDER")
sys.path.insert(0, str(PROJECT_DIR / "src"))

from controller import Controller

INVENTORY_ITEMS_SHEET: str = "products"
ORDERS_SHEET: str = "orders"


def get_sheet(sheets: Any, name: str) -> Any:
    present: bool = sheets.hasByName(name)
    if not present:
        raise ValueError(f"Sheet {name} does not exist")
    return sheets.getByName(name)


def write_sheet(sheet: Any, data: Iterable[Iterable[Any]]) -> None:
    # TODO: Delete all data before writing data
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            cell = sheet.getCellByPosition(x, y)
            cell.String = value


def main() -> None:
    controller: Controller = Controller(PROJECT_DIR)
    controller.update_inventory_items()
    controller.update_orders()
    doc = XSCRIPTCONTEXT.getDocument()  # type: ignore
    sheets = doc.getSheets()
    write_sheet(
        sheet=get_sheet(sheets, INVENTORY_ITEMS_SHEET),
        data=controller.get_inventory_items(),
    )
    write_sheet(
        sheet=get_sheet(sheets, ORDERS_SHEET),
        data=controller.get_orders(),
    )
    return
