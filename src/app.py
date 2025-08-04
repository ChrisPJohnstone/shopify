#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
import logging

from controller import Controller


def main() -> None:
    controller: Controller = Controller()
    controller.update_inventory_items()
    controller.update_orders()


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    main()
