from __future__ import annotations

from typing import Any, Callable, Dict, TYPE_CHECKING

from hstest.dynamic.input.dynamic_input_handler import DynamicInputHandler
from hstest.dynamic.security.exit_exception import ExitException
from hstest.dynamic.security.thread_group import ThreadGroup
from hstest.exception.outcomes import OutOfInputError, UnexpectedError
from hstest.testing.settings import Settings

if TYPE_CHECKING:
    from hstest.dynamic.input.dynamic_input_func import DynamicTestFunction

    Condition = Callable[[], bool]


class ConditionalInputHandler:
    def __init__(self, condition: Condition, handler: DynamicInputHandler):
        self.condition = condition
        self.handler = handler


class InputMock:
    def __init__(self):
        self.handlers: Dict[ThreadGroup, ConditionalInputHandler] = {}

    def install_input_handler(self, obj: Any, condition: Condition,
                              input_func: DynamicTestFunction):
        if obj in self.handlers:
            raise UnexpectedError("Cannot install input handler from the same program twice")
        self.handlers[obj] = ConditionalInputHandler(
            condition,
            DynamicInputHandler(input_func)
        )

    def uninstall_input_handler(self, obj: Any):
        if obj not in self.handlers:
            raise UnexpectedError("Cannot uninstall input handler that doesn't exist")
        del self.handlers[obj]

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
                StageTest.curr_test_run.set_error_in_test(OutOfInputError())
                raise ExitException()
            else:
                raise EOFError('EOF when reading a line')
        return line
