from typing import Callable, List, Optional, Union
from hstest.dynamic.handle_stdout import StdoutHandler
from hstest.check_result import CheckResult
from hstest.exceptions import TestPassed
from hstest.exceptions import WrongAnswer
from hstest.exceptions import FatalErrorException
from hstest.utils import clear_text
from hstest.test_run import TestRun

InputFunction = Callable[[str], Union[str, CheckResult]]


class DynamicInputFunction:
    def __init__(self, trigger_count: int, func: InputFunction):
        self.trigger_count = trigger_count
        self.input_function = func


class InputMock:
    def __init__(self):
        self.input_lines: List[str] = []
        self.input_text_funcs: List[DynamicInputFunction] = []

    def provide_text(self, text: str):
        texts = [DynamicInputFunction(1, lambda t, saved=text: saved)]
        self.set_texts(texts)

    def set_texts(self, texts: List[DynamicInputFunction]):
        self.input_lines = []
        self.input_text_funcs = texts

    def readline(self):
        test_run = TestRun.curr_test_run

        if test_run is not None and test_run.error_in_test is not None:
            raise EOFError('EOF when reading a line')

        if test_run is None or test_run.error_in_test is None:
            next_line = self.eject_next_line()
            if next_line is not None:
                return next_line

        raise EOFError('EOF when reading a line')

    def eject_next_line(self) -> Optional[str]:
        if len(self.input_lines) == 0:
            self.input_lines = self.eject_next_input()
            if len(self.input_lines) == 0:
                return None

        next_line = self.input_lines.pop(0) + '\n'
        StdoutHandler.inject_input('> ' + next_line)
        return next_line

    def eject_next_input(self) -> List[str]:
        if len(self.input_text_funcs) == 0:
            return []

        input_function = self.input_text_funcs[0]
        if input_function.trigger_count > 0:
            input_function.trigger_count -= 1

        curr_output = StdoutHandler.get_partial_output()
        next_func = input_function.input_function

        new_input: str
        try:
            obj = next_func(curr_output)
            if isinstance(obj, str):
                new_input = obj
            elif isinstance(obj, CheckResult):
                if obj.result:
                    raise TestPassed()
                else:
                    raise WrongAnswer(obj.feedback)
            else:
                raise FatalErrorException(
                    'Dynamic input should return ' +
                    f'str or CheckResult objects only. Found: {type(obj)}')
        except BaseException as ex:
            TestRun.curr_test_run.error_in_test = ex
            return []

        if input_function.trigger_count == 0:
            self.input_text_funcs.pop(0)

        new_input = clear_text(new_input)
        return new_input.strip().split('\n')
