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


class LibreCalc:
    """
    Type hints are pretty meaningless because of poor support from library
    """

    def __init__(self) -> None:
        self.doc: Any = XSCRIPTCONTEXT.getDocument()  # type: ignore
        self.sheets: Any = self.doc.getSheets()

    def get_sheet(self, name: str) -> Any:
        present: bool = self.sheets.hasByName(name)
        if not present:
            raise ValueError(f"Sheet {name} does not exist")
        return self.sheets.getByName(name)

    def write_sheet(self, sheet: Any, data: Iterable[Iterable[Any]]) -> None:
        # TODO: Delete all data before writing data
        for y, row in enumerate(data):
            for x, value in enumerate(row):
                cell = sheet.getCellByPosition(x, y)
                cell.String = value


def main() -> None:
    controller: Controller = Controller(PROJECT_DIR)
    controller.update_inventory_items()
    controller.update_orders()
    spreadsheet_client: LibreCalc = LibreCalc()
    spreadsheet_client.write_sheet(
        sheet=spreadsheet_client.get_sheet(INVENTORY_ITEMS_SHEET),
        data=controller.get_inventory_items(),
    )
    spreadsheet_client.write_sheet(
        sheet=spreadsheet_client.get_sheet(ORDERS_SHEET),
        data=controller.get_orders(),
    )
    return
