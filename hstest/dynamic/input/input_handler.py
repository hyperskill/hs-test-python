import io
import sys
import typing

from hstest.dynamic.input.input_mock import Condition, InputMock

if typing.TYPE_CHECKING:
    from hstest.testing.execution.program_executor import ProgramExecutor


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
    def install_input_handler(program: 'ProgramExecutor', condition: Condition):
        InputHandler.mock_in.install_input_handler(program, condition)

    @staticmethod
    def uninstall_input_handler(program: 'ProgramExecutor'):
        InputHandler.mock_in.uninstall_input_handler(program)
