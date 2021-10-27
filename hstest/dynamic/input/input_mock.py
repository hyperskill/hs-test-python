from typing import Callable, Dict

from hstest.dynamic.input.dynamic_input_handler import DynamicInputHandler
from hstest.dynamic.security.exit_exception import ExitException
from hstest.exception.outcomes import ErrorWithFeedback, UnexpectedError
from hstest.testing.execution.program_executor import ProgramExecutor
from hstest.testing.settings import Settings

Condition = Callable[[], bool]


class ConditionalInputHandler:
    def __init__(self, condition: Condition, handler: DynamicInputHandler):
        self.condition = condition
        self.handler = handler


class InputMock:
    def __init__(self):
        self.handlers: Dict[ProgramExecutor, ConditionalInputHandler] = {}

    def install_input_handler(self, program: ProgramExecutor, condition: Condition):
        if program in self.handlers:
            raise UnexpectedError("Cannot install input handler from the same program twice")
        self.handlers[program] = ConditionalInputHandler(
            condition,
            DynamicInputHandler(lambda: program.request_input())
        )

    def uninstall_input_handler(self, program: ProgramExecutor):
        if program not in self.handlers:
            raise UnexpectedError("Cannot uninstall input handler that doesn't exist")
        del self.handlers[program]

    def __get_input_handler(self) -> DynamicInputHandler:
        for handler in self.handlers.values():
            if handler.condition():
                return handler.handler

        from hstest import StageTest
        StageTest.curr_test_run.set_error_in_test(UnexpectedError(
            "Cannot find input handler to read data"))
        raise ExitException()

    def readline(self) -> str:
        line = self.__get_input_handler().eject_next_line()
        if line is None:
            if not Settings.allow_out_of_input:
                from hstest import StageTest
                StageTest.curr_test_run.set_error_in_test(ErrorWithFeedback(
                    "Program ran out of input. You tried to read more than expected."))
                raise ExitException()
            else:
                raise EOFError('EOF when reading a line')
        return line
