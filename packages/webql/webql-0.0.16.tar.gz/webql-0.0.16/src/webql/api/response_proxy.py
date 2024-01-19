import json
from typing import Generic

from webql.common.aria_constants import CHECKBOX_ROLES, CLICKABLE_ROLES, INPUT_ROLES
from webql.common.errors import AttributeNotFoundError
from webql.web import InteractiveItemTypeT, WebDriver


class WQLResponseProxy(Generic[InteractiveItemTypeT]):
    def __init__(self, data: dict, web_driver: "WebDriver[InteractiveItemTypeT]"):
        self._response_data = data
        self._web_driver = web_driver

    def __getattr__(self, name) -> "WQLResponseProxy[InteractiveItemTypeT]" | InteractiveItemTypeT:
        if name not in self._response_data:
            raise AttributeNotFoundError(name, self._response_data)

        return self._resolve_item(self._response_data[name])

    def __getitem__(
        self, index: int
    ) -> InteractiveItemTypeT | "WQLResponseProxy[InteractiveItemTypeT]":
        if not isinstance(self._response_data, list):
            raise ValueError("This node is not a list")
        return self._resolve_item(self._response_data[index])

    def _resolve_item(
        self, item
    ) -> InteractiveItemTypeT | "WQLResponseProxy[InteractiveItemTypeT]":
        if isinstance(item, list):
            return WQLResponseProxy[InteractiveItemTypeT](item, self._web_driver)
        if _is_clickable(item) or _is_text_input(item) or _is_checkbox(item):
            return self._web_driver.locate_interactive_element(item)
        if isinstance(item, dict):
            return WQLResponseProxy[InteractiveItemTypeT](item, self._web_driver)

        raise ValueError(f"Unknown node type: {item}")

    def __len__(self):
        return len(self._response_data)

    def __str__(self):
        return json.dumps(self._response_data, indent=2)


def _is_clickable(node: dict) -> bool:
    return node.get("role") in CLICKABLE_ROLES


def _is_text_input(node: dict) -> bool:
    return node.get("role") in INPUT_ROLES


def _is_checkbox(node: dict) -> bool:
    return node.get("role") in CHECKBOX_ROLES
