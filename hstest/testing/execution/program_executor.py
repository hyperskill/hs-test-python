from enum import Enum
from typing import Optional

from hstest.exception.outcomes import UnexpectedError, ErrorWithFeedback
from hstest.exception.testing import TestedProgramFinishedEarly, TestedProgramThrewException
from hstest.testing.state_machine import StateMachine


class ProgramState(Enum):
    NOT_STARTED = 1
    WAITING = 2
    RUNNING = 3
    EXCEPTION_THROWN = 4
    FINISHED = 5


class ProgramExecutor:
    def __init__(self):
        self._input: Optional[str] = None

        self.__in_background: bool = False
        self.__no_more_input: bool = False
        self.__return_output_after_execution: bool = True
        self._machine: StateMachine = StateMachine(ProgramState.NOT_STARTED)

        m = self._machine
        m.add_transition(ProgramState.NOT_STARTED, ProgramState.RUNNING)
        m.add_transition(ProgramState.WAITING, ProgramState.RUNNING)
        m.add_transition(ProgramState.RUNNING, ProgramState.WAITING)
        m.add_transition(ProgramState.RUNNING, ProgramState.EXCEPTION_THROWN)
        m.add_transition(ProgramState.RUNNING, ProgramState.FINISHED)

    def _launch(self, *args: str):
        raise NotImplementedError('Method "_launch" isn\'t implemented')

    def get_output(self) -> str:
        raise NotImplementedError('Method "get_output" isn\'t implemented')

    def stop(self):
        raise NotImplementedError('Method "get_output" isn\'t implemented')

    def start(self, *args: str):
        if not self._machine.in_state(ProgramState.NOT_STARTED):
            raise UnexpectedError(
                "Cannot start the program " + str(self) + " twice")

        self._launch(*args)

        if self.__in_background:
            self._machine.wait_not_state(ProgramState.NOT_STARTED)
            return ""

        self._machine.wait_not_states(
            ProgramState.NOT_STARTED, ProgramState.RUNNING)

        return self.__get_execution_output()

    def execute(self, stdin: str) -> str:
        if self.is_finished():
            from hstest.stage_test import StageTest
            StageTest.curr_test_run.set_error_in_test(ErrorWithFeedback(
                    "The program " + str(self) + " has unexpectedly terminated.\n" +
                    "It finished execution too early, should continue running."))
            raise TestedProgramFinishedEarly()

        if stdin is None:
            self.stop_input()
            return ""

        if not self.is_waiting_input():
            raise UnexpectedError(
                "Program " + str(self) + " is not waiting for the input "
                + "(state == \"" + str(self._machine.state) + "\")")

        if self.__no_more_input:
            raise UnexpectedError(
                "Can't pass input to the program " + str(self)
                + " - input was prohibited.")

        self._input = stdin
        if self.__in_background:
            self._machine.set_state(ProgramState.RUNNING)
            return ""

        # suspends thread while the program is executing,
        # waits for non-RUNNING state to be reached
        self._machine.set_and_wait(ProgramState.RUNNING)
        return self.__get_execution_output()

    def __get_execution_output(self) -> str:
        if self._machine.in_state(ProgramState.EXCEPTION_THROWN):
            raise TestedProgramThrewException()

        if self.__return_output_after_execution:
            return self.get_output()
        return ""

    def _request_input(self):
        if self.__no_more_input:
            return None
        self._machine.set_and_wait(ProgramState.WAITING, ProgramState.RUNNING)
        input_local = self._input
        self._input = None
        return input_local

    def set_return_output_after_execution(self, value: bool):
        self.__return_output_after_execution = value

    def is_finished(self) -> bool:
        finished = self._machine.in_state(ProgramState.FINISHED)
        exception = self._machine.in_state(ProgramState.EXCEPTION_THROWN)
        return finished or exception

    def stop_input(self):
        self.__in_background = True
        self.__no_more_input = True
        if self.is_waiting_input():
            self._machine.set_state(ProgramState.RUNNING)

    def is_waiting_input(self) -> bool:
        return self._machine.in_state(ProgramState.WAITING)

    def start_in_background(self, *args: str):
        self.__in_background = True
        self.start(*args)

    def go_background(self):
        self.__in_background = True

    def stop_background(self):
        self.__in_background = False
        self._machine.wait_state(ProgramState.WAITING)

    def is_in_background(self):
        return self.__in_background

    def __str__(self) -> str:
        raise NotImplementedError('Method "__str__" isn\'t implemented')
