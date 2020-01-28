import io
import os
import builtins
import sys
import signal
from typing import List
from hstest.dynamic.stdout import OutputMock
from hstest.dynamic.stdin import InputMock
from hstest.dynamic.stdin import DynamicInputFunction
from hstest.utils import normalize_line_endings
from hstest.exceptions import ExitException
from hstest.test_run import TestRun


class SystemHandler:
    @staticmethod
    def set_up():
        StdoutHandler.replace_stdout()
        StdinHandler.replace_stdin()
        ExitHandler.replace_exit()

    @staticmethod
    def tear_down():
        StdoutHandler.revert_stdout()
        StdinHandler.revert_stdin()
        ExitHandler.revert_exit()




