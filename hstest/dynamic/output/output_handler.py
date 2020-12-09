import io
import sys

from hstest.dynamic.output.output_mock import OutputMock
from hstest.common.utils import clear_text


class OutputHandler:
    _real_out: io.TextIOWrapper = None
    _real_err: io.TextIOWrapper = None

    _mock_out: OutputMock = None
    _mock_err: OutputMock = None

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
        return clear_text(OutputHandler._mock_out.cloned)

    @staticmethod
    def get_dynamic_output() -> str:
        return clear_text(OutputHandler._mock_err.dynamic)

    @staticmethod
    def get_partial_output() -> str:
        return clear_text(OutputHandler._mock_err.partial)

    @staticmethod
    def inject_input(user_input: str):
        from hstest.stage_test import StageTest
        if StageTest.curr_test_run is not None:
            StageTest.curr_test_run.set_input_used()
        OutputHandler._mock_out.inject_input(user_input)
