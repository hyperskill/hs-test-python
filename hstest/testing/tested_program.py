from __future__ import annotations

from typing import TYPE_CHECKING

from hstest.exception.outcomes import UnexpectedError

if TYPE_CHECKING:
    from hstest.testing.execution.program_executor import ProgramExecutor


class TestedProgram:
    def __init__(self, source: str | None = None) -> None:
        from hstest import StageTest

        runner = StageTest.curr_test_run.test_runner

        from hstest.testing.runner.async_dynamic_testing_runner import AsyncDynamicTestingRunner

        if not isinstance(runner, AsyncDynamicTestingRunner):
            raise UnexpectedError(
                "TestedProgram is supported only while using AsyncDynamicTestingRunner runner, "
                "not " + str(type(runner))
            )

        if source is None:
            from hstest.stage_test import StageTest

            source = StageTest.curr_test_run.test_case.source_name

        self._program_executor: ProgramExecutor = runner.executor(source)
        self._run_args: list[str] | None = None

    @property
    def run_args(self):
        return self._run_args

    @property
    def executor(self):
        return self._program_executor

    def _init_program(self, *args: str) -> None:
        self._run_args = args
        from hstest.stage_test import StageTest

        if StageTest.curr_test_run:
            StageTest.curr_test_run.add_tested_program(self)

    def feedback_on_exception(self, ex: type[Exception], feedback: str) -> None:
        from hstest import StageTest

        StageTest.curr_test_run.test_case.feedback_on_exception[ex] = feedback

    def start_in_background(self, *args: str) -> None:
        self._init_program(*args)
        self._program_executor.start_in_background(*args)

    def start(self, *args: str) -> str:
        self._init_program(*args)
        return self._program_executor.start(*args)

    def execute(self, stdin: str | None) -> str:
        return self._program_executor.execute(stdin)

    def get_output(self) -> str:
        return self._program_executor.get_output()

    def stop(self) -> None:
        self._program_executor.stop()

    def is_finished(self) -> bool:
        return self._program_executor.is_finished()

    def set_return_output_after_execution(self, value: bool) -> None:
        self._program_executor.set_return_output_after_execution(value)

    def stop_input(self) -> None:
        self._program_executor.stop_input()

    def is_input_allowed(self) -> bool:
        return self._program_executor.is_input_allowed()

    def is_waiting_input(self) -> bool:
        return self._program_executor.is_waiting_input()

    def go_background(self) -> None:
        self._program_executor.go_background()

    def stop_background(self) -> None:
        self._program_executor.stop_background()

    def is_in_background(self) -> bool:
        return self._program_executor.is_in_background()

    def __str__(self) -> str:
        return str(self._program_executor)
