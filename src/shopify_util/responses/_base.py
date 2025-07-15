import json
import logging

from type_definitions import JSONObject


class Base:
    def __init__(self, value: JSONObject) -> None:
        logging.debug(value)
        self.__node: JSONObject = value

    @property
    def _node(self) -> JSONObject:
        return self.__node

    def __repr__(self) -> str:
        return json.dumps(self._node, indent=2)
