#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
import logging

from controller import Controller


def main() -> None:
    controller: Controller = Controller()
    for x, row in enumerate(controller.get_inventory_items()):
        print(x, row)
    # controller.get_orders()


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    args: Namespace = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    main()
