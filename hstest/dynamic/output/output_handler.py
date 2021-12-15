import io
import sys
from typing import Any, TYPE_CHECKING

from hstest.common.utils import clean_text
from hstest.dynamic.output.colored_output import BLUE, RESET
from hstest.dynamic.output.output_mock import OutputMock
from hstest.dynamic.security.thread_group import ThreadGroup

if TYPE_CHECKING:
    from hstest.dynamic.input.input_mock import Condition


class OutputHandler:
    _real_out: io.TextIOWrapper = None
    _real_err: io.TextIOWrapper = None

    _mock_out: OutputMock = None
    _mock_err: OutputMock = None

    @staticmethod
    def print(obj):
        if True:
            return

        lines = obj.strip().split('\n')

        group = ThreadGroup.curr_group()

        if group:
            name = group.name
        else:
            name = "Root"

        prepend = f'[{name}] '

        output = prepend + ('\n' + prepend).join(lines)
        full = BLUE + output + '\n' + RESET

        if group:
            OutputHandler.get_real_out().write(full)
            OutputHandler.get_real_out().flush()
        else:
            print(full, end='')

    @staticmethod
    def get_real_out() -> io.TextIOWrapper:
        return OutputHandler._mock_out.original

    @staticmethod
    def get_real_err() -> io.TextIOWrapper:
        return OutputHandler._mock_err.original

    @staticmethod
    def replace_stdout():
        OutputHandler._real_out = sys.stdout
        OutputHandler._real_err = sys.stderr

        OutputHandler._mock_out = OutputMock(sys.stdout)
        OutputHandler._mock_err = OutputMock(sys.stderr)

        sys.stdout = OutputHandler._mock_out
        sys.stderr = OutputHandler._mock_err

    @staticmethod
    def revert_stdout():
        OutputHandler.reset_output()
        sys.stdout = OutputHandler._real_out
        sys.stderr = OutputHandler._real_err

    @staticmethod
    def reset_output():
        OutputHandler._mock_out.reset()
        OutputHandler._mock_err.reset()

    @staticmethod
    def get_output() -> str:
        return clean_text(OutputHandler._mock_out.cloned)

    @staticmethod
    def get_err() -> str:
        return clean_text(OutputHandler._mock_err.cloned)

    @staticmethod
    def get_dynamic_output() -> str:
        return clean_text(OutputHandler._mock_out.dynamic)

    @staticmethod
    def get_partial_output(obj: Any) -> str:
        return clean_text(OutputHandler._mock_out.partial(obj))

    @staticmethod
    def inject_input(user_input: str):
        from hstest.stage_test import StageTest
        if StageTest.curr_test_run is not None:
            StageTest.curr_test_run.set_input_used()
        OutputHandler._mock_out.inject_input(user_input)

    @staticmethod
    def install_output_handler(obj: Any, condition: 'Condition'):
        OutputHandler._mock_out.install_output_handler(obj, condition)
        OutputHandler._mock_err.install_output_handler(obj, condition)

    @staticmethod
    def uninstall_output_handler(obj: Any):
        OutputHandler._mock_out.uninstall_output_handler(obj)
        OutputHandler._mock_err.uninstall_output_handler(obj)
