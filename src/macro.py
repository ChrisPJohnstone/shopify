#!/usr/bin/env python3
from __future__ import unicode_literals
from pathlib import Path
import sys

PROJECT_DIR: Path = Path("PATH_PLACEHOLDER")
sys.path.insert(0, str(PROJECT_DIR / "src"))

import uno

from controller import Controller


def main() -> None:
    controller: Controller = Controller(PROJECT_DIR)
    controller.update_inventory_items()
    controller.update_orders()
    doc = XSCRIPTCONTEXT.getDocument()  # type: ignore
    sheet = doc.getSheets().getByIndex(0)
    cell = sheet.getCellByPosition(0, 0)
    cell.String = "test"
    return
