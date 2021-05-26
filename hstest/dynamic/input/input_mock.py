from typing import List

from hstest.dynamic.input.dynamic_input_func import DynamicInputFunction, DynamicTestFunction
from hstest.dynamic.input.dynamic_input_handler import DynamicInputHandler
from hstest.dynamic.security.exit_exception import ExitException
from hstest.exception.outcomes import ErrorWithFeedback
from hstest.testing.settings import Settings


class InputMock:
    def __init__(self):
        # self.input_lines: List[str] = []
        # self.input_text_funcs: List[DynamicInputFunction] = []
        self.handler: DynamicInputHandler = DynamicInputHandler(lambda: "")

    def provide_text(self, text: str):
        """
        Deprecated
        """
        texts = [DynamicInputFunction(1, lambda t, saved=text: saved)]
        self.set_texts(texts)

    def set_texts(self, texts: List[DynamicInputFunction]):
        """
        Deprecated
        """
        self.input_lines = []
        self.input_text_funcs = texts

    def set_dynamic_input_func(self, func: DynamicTestFunction):
        self.handler = DynamicInputHandler(func)

    def readline(self) -> str:
        line = self.handler.eject_next_line()
        if line is None:
            if not Settings.allow_out_of_input:
                from hstest import StageTest
                StageTest.curr_test_run.set_error_in_test(ErrorWithFeedback(
                    "Program ran out of input. You tried to read more than expected."))
                raise ExitException()
            else:
                raise EOFError('EOF when reading a line')
        return line
