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

    def clear_sheet(self, sheet: Any) -> None:
        cursor: Any = sheet.createCursor()
        cursor.gotoEndOfUsedArea(False)
        cursor.gotoStartOfUsedArea(True)
        used_range: Any = cursor.getRangeAddress()
        if used_range.EndRow == 0:
            return
        sheet.getCellRangeByPosition(
            0,
            1,
            used_range.EndColumn,
            used_range.EndRow,
        ).clearContents(1023)

    def write_sheet(self, sheet: Any, data: Iterable[Iterable[Any]]) -> None:
        self.clear_sheet(sheet)
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
