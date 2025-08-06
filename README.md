# Overview

Shopify scripts built using Python standard library.

## Why / Background

I'm helping a relative with managing their business, currently the project is just to keep track of profitability, due to heavy need for manual data entry (limitations in the fields available in Shopify) and my lack of desire to build a front end this code is primarily designed to run as macros in LibreOffice Calc.

# Usage

- `src/local.py` Runs as a standard python file (e.g. `python src/local.py`)
- `src/macro.py` Is intended to be used by LibreOffice Calc as a macro
    - Can be added to libreoffice scripts using `./scripts/add_to_libreoffice`

# Spreadsheet Notes

- Macro works on open document
    *Tools > Customize > Open Document*
