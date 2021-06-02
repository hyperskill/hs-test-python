from typing import List, Optional

from hstest.exception.outcomes import UnexpectedError
from hstest.testing.execution.program_executor import ProgramExecutor


class TestedProgram:
    def __init__(self, source: str = None):
        from hstest import StageTest
        runner = StageTest.curr_test_run.test_runner

        from hstest.testing.runner.async_main_file_runner import AsyncMainFileRunner
        if not isinstance(runner, AsyncMainFileRunner):
            raise UnexpectedError(
                'TestedProgram is supported only while using AsyncMainFileRunner runner, '
                'not ' + str(type(runner))
            )

        self._program_executor: ProgramExecutor = runner.executor(source)
        self._run_args: Optional[List[str]] = None

    @property
    def run_args(self):
        return self._run_args

    def _init_program(self, *args: str):
        self._run_args = args
        from hstest.stage_test import StageTest
        if StageTest.curr_test_run:
            StageTest.curr_test_run.add_tested_program(self)

    def start_in_background(self, *args: str):
        self._init_program(*args)
        self._program_executor.start_in_background(*args)

    def start(self, *args: str) -> str:
        self._init_program(*args)
        return self._program_executor.start(*args)

    def execute(self, stdin: Optional[str]) -> str:
        return self._program_executor.execute(stdin)

    def get_output(self) -> str:
        return self._program_executor.get_output()

    def stop(self):
        self._program_executor.stop()

    def is_finished(self) -> bool:
        return self._program_executor.is_finished()

    def set_return_output_after_execution(self, value: bool):
        self._program_executor.set_return_output_after_execution(value)

    def stop_input(self):
        self._program_executor.stop_input()

    def is_input_allowed(self) -> bool:
        return self._program_executor.is_input_allowed()

    def is_waiting_input(self) -> bool:
        return self._program_executor.is_waiting_input()

    def go_background(self):
        self._program_executor.go_background()

    def stop_background(self):
        self._program_executor.stop_background()

    def is_in_background(self) -> bool:
        return self._program_executor.is_in_background()

    def __str__(self) -> str:
        return str(self._program_executor)
