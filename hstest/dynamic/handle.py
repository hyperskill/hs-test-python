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


class StdoutHandler:
    real_stdout: io.TextIOWrapper = sys.stdout
    mock_stdout: 'OutputMock' = OutputMock(real_stdout)

    @staticmethod
    def replace_stdout():
        sys.stdout = StdoutHandler.mock_stdout

    @staticmethod
    def revert_stdout():
        StdoutHandler.reset_output()
        sys.stdout = StdoutHandler.real_stdout

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
        # todo add test run check
        StdoutHandler.mock_stdout.inject_input(user_input)


class StdinHandler:
    real_stdin: io.TextIOWrapper = sys.stdin
    mock_stdin: 'InputMock' = InputMock()

    @staticmethod
    def replace_stdin():
        sys.stdin = StdinHandler.mock_stdin

    @staticmethod
    def revert_stdin():
        sys.stdin = StdinHandler.real_stdin

    @staticmethod
    def set_input(text: str):
        StdinHandler.mock_stdin.provide_text(text)

    @staticmethod
    def set_input_funcs(input_funcs: List[DynamicInputFunction]):
        StdinHandler.mock_stdin.set_texts([
            DynamicInputFunction(func.trigger_count, func.input_function)
            for func in input_funcs
        ])


class ExitHandler:
    _builtins_quit = builtins.quit
    _builtins_exit = builtins.exit
    _os_kill = os.kill
    _os__exit = os._exit
    _os_killpg = os.killpg
    _signal_pthread_kill = signal.pthread_kill
    _signal_siginterrupt = signal.siginterrupt

    _exit_func = lambda *x, **y: ExitException.throw()

    @staticmethod
    def replace_exit():
        builtins.quit = ExitHandler._exit_func
        builtins.exit = ExitHandler._exit_func
        os.kill = ExitHandler._exit_func
        os._exit = ExitHandler._exit_func
        os.killpg = ExitHandler._exit_func
        signal.pthread_kill = ExitHandler._exit_func
        signal.siginterrupt = ExitHandler._exit_func

    @staticmethod
    def revert_exit():
        builtins.quit = ExitHandler._builtins_quit
        builtins.exit = ExitHandler._builtins_exit
        os.kill = ExitHandler._os_kill
        os._exit = ExitHandler._os__exit
        os.killpg = ExitHandler._os_killpg
        signal.pthread_kill = ExitHandler._signal_pthread_kill
        signal.siginterrupt = ExitHandler._signal_siginterrupt
