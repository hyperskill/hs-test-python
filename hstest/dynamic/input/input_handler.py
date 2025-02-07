from __future__ import annotations

import sys
from typing import Any, TYPE_CHECKING

from hstest.dynamic.input.input_mock import InputMock

if TYPE_CHECKING:
    import io

    from hstest.dynamic.input.dynamic_input_func import DynamicTestFunction
    from hstest.dynamic.input.input_mock import Condition


class InputHandler:
    real_in: io.TextIOWrapper = sys.stdin
    mock_in: InputMock = InputMock()

    @staticmethod
    def replace_input() -> None:
        sys.stdin = InputHandler.mock_in

    @staticmethod
    def revert_input() -> None:
        sys.stdin = InputHandler.real_in

    @staticmethod
    def install_input_handler(
        obj: Any, condition: Condition, input_func: DynamicTestFunction
    ) -> None:
        InputHandler.mock_in.install_input_handler(obj, condition, input_func)

    @staticmethod
    def uninstall_input_handler(obj: Any) -> None:
        InputHandler.mock_in.uninstall_input_handler(obj)
