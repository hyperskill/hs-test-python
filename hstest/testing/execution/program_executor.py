from __future__ import annotations

from enum import Enum
from typing import NoReturn

from hstest.dynamic.output.output_handler import OutputHandler
from hstest.exception.outcomes import ErrorWithFeedback, UnexpectedError
from hstest.exception.testing import TestedProgramFinishedEarly, TestedProgramThrewException
from hstest.testing.state_machine import StateMachine


class ProgramState(Enum):
    NOT_STARTED = 1
    WAITING = 2
    RUNNING = 3
    EXCEPTION_THROWN = 4
    FINISHED = 5
    COMPILATION_ERROR = 6


class ProgramExecutor:
    def __init__(self, source_name: str | None = None) -> None:
        self._input: str | None = None

        self.__in_background: bool = False
        self.__no_more_input: bool = False
        self.__return_output_after_execution: bool = True
        self._machine: StateMachine = StateMachine(ProgramState.NOT_STARTED)

        m = self._machine
        m.add_transition(ProgramState.NOT_STARTED, ProgramState.COMPILATION_ERROR)
        m.add_transition(ProgramState.NOT_STARTED, ProgramState.RUNNING)
        m.add_transition(ProgramState.WAITING, ProgramState.RUNNING)
        m.add_transition(ProgramState.RUNNING, ProgramState.WAITING)
        m.add_transition(ProgramState.RUNNING, ProgramState.EXCEPTION_THROWN)
        m.add_transition(ProgramState.RUNNING, ProgramState.FINISHED)

    def _launch(self, *args: str) -> NoReturn:
        msg = 'Method "_launch" isn\'t implemented'
        raise NotImplementedError(msg)

    def _terminate(self) -> NoReturn:
        msg = 'Method "_terminate" isn\'t implemented'
        raise NotImplementedError(msg)

    def get_output(self) -> str:
        return OutputHandler.get_partial_output(self)

    def start(self, *args: str) -> str:
        if not self._machine.in_state(ProgramState.NOT_STARTED):
            msg = f"Cannot start the program {self} twice"
            raise UnexpectedError(msg)

        self._launch(*args)

        if self.__in_background:
            self._machine.wait_not_state(ProgramState.NOT_STARTED)
            return ""

        self._machine.wait_not_states(ProgramState.NOT_STARTED, ProgramState.RUNNING)

        OutputHandler.print("Program executor - after waiting in start() method")

        return self.__get_execution_output()

    def execute(self, stdin: str) -> str:
        if self.is_finished():
            from hstest.stage_test import StageTest

            StageTest.curr_test_run.set_error_in_test(
                ErrorWithFeedback(
                    f"The program {self} has unexpectedly terminated.\n"
                    + "It finished execution too early, should continue running."
                )
            )
            raise TestedProgramFinishedEarly

        if stdin is None:
            self.stop_input()
            return ""

        if not self.is_waiting_input():
            raise UnexpectedError(
                f"Program {self} is not waiting for the input "
                + f'(state == "{self._machine.state}")'
            )

        if self.__no_more_input:
            msg = f"Can't pass input to the program {self} - input was prohibited."
            raise UnexpectedError(msg)

        self._input = stdin
        if self.__in_background:
            self._machine.set_state(ProgramState.RUNNING)
            return ""

        # suspends thread while the program is executing,
        # waits for non-RUNNING state to be reached
        self._machine.set_and_wait(ProgramState.RUNNING)
        return self.__get_execution_output()

    def stop(self) -> None:
        self.__no_more_input = True
        self._terminate()

    def __get_execution_output(self) -> str:
        OutputHandler.print("Program executor - __get_execution_output()")
        if self._machine.in_state(ProgramState.EXCEPTION_THROWN):
            raise TestedProgramThrewException
        OutputHandler.print("Program executor - __get_execution_output() NO EXCEPTION")
        if self.__return_output_after_execution:
            return self.get_output()
        return ""

    def request_input(self) -> str | None:
        if self.__no_more_input:
            return None
        OutputHandler.print(
            "Program executor - _request_input() invoked, set state WAITING"
        )
        self._machine.set_and_wait(ProgramState.WAITING, ProgramState.RUNNING)
        input_local = self._input
        self._input = None
        return input_local

    def set_return_output_after_execution(self, value: bool) -> None:
        self.__return_output_after_execution = value

    def is_finished(self) -> bool:
        finished = self._machine.in_state(ProgramState.FINISHED)
        exception = self._machine.in_state(ProgramState.EXCEPTION_THROWN)
        return finished or exception

    def stop_input(self) -> None:
        self.__in_background = True
        self.__no_more_input = True
        if self.is_waiting_input():
            self._machine.set_state(ProgramState.RUNNING)

    def is_input_allowed(self) -> bool:
        return not self.__no_more_input

    def is_waiting_input(self) -> bool:
        return self._machine.in_state(ProgramState.WAITING)

    def start_in_background(self, *args: str) -> None:
        self.__in_background = True
        self.start(*args)

    def go_background(self) -> None:
        self.__in_background = True

    def stop_background(self) -> None:
        self.__in_background = False
        self._machine.wait_state(ProgramState.WAITING)

    def is_in_background(self):
        return self.__in_background

    def tear_down(self) -> None:
        pass

    def __str__(self) -> str:
        msg = 'Method "__str__" isn\'t implemented'
        raise NotImplementedError(msg)
