import io
import sys
from hstest.dynamic.stdout import OutputMock
from hstest.test_run import TestRun
from hstest.utils import normalize_line_endings


class StdoutHandler:
    real_stdout: io.TextIOWrapper = sys.stdout
    mock_stdout: OutputMock = OutputMock(real_stdout)

    @staticmethod
    def replace_stdout():
        sys.stdout = StdoutHandler.mock_stdout

    @staticmethod
    def revert_stdout():
        StdoutHandler.reset_output()
        sys.stdout = StdoutHandler.real_stdout
        #sys.stdout.getvalue = lambda *a, **k: ''  # PyCharm cannot test without defining getvalue

    @staticmethod
    def reset_output():
        StdoutHandler.mock_stdout.reset()

    @staticmethod
    def get_output() -> str:
        return normalize_line_endings(
            ''.join(StdoutHandler.mock_stdout.cloned))

    @staticmethod
    def get_partial_output() -> str:
        output = normalize_line_endings(
            ''.join(StdoutHandler.mock_stdout.partial))
        StdoutHandler.mock_stdout.partial = []
        return output

    @staticmethod
    def get_dynamic_output() -> str:
        return normalize_line_endings(
            ''.join(StdoutHandler.mock_stdout.dynamic))

    @staticmethod
    def inject_input(user_input: str):
        if TestRun.curr_test_run is not None:
            TestRun.curr_test_run.input_used = True
        StdoutHandler.mock_stdout.inject_input(user_input)
