import io
import sys
from typing import Any, TYPE_CHECKING

from hstest.dynamic.input.input_mock import InputMock

if TYPE_CHECKING:
    from hstest.dynamic.input.dynamic_input_func import DynamicTestFunction
    from hstest.dynamic.input.input_mock import Condition


class InputHandler:
    real_in: io.TextIOWrapper = sys.stdin
    mock_in: InputMock = InputMock()

    @staticmethod
    def replace_input():
        sys.stdin = InputHandler.mock_in

    @staticmethod
    def revert_input():
        sys.stdin = InputHandler.real_in

    @staticmethod
    def install_input_handler(obj: Any, condition: 'Condition', input_func: 'DynamicTestFunction'):
        InputHandler.mock_in.install_input_handler(obj, condition, input_func)

    @staticmethod
    def uninstall_input_handler(obj: Any):
        InputHandler.mock_in.uninstall_input_handler(obj)
