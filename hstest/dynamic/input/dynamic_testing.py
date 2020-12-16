from typing import Any, Callable, List, Optional, Tuple

from hstest.check_result import CheckResult
from hstest.common.utils import clean_text
from hstest.dynamic.input.dynamic_input_func import DynamicInputFunction
from hstest.exception.outcomes import UnexpectedError
from hstest.exceptions import TestPassed, WrongAnswer
from hstest.testing.tested_program import TestedProgram

DynamicTesting = Callable[[], Optional[CheckResult]]
DynamicTestingWithoutParams = Callable[[List[Any]], Optional[CheckResult]]


class DynamicTestElement:
    def __init__(self,
                 test: DynamicTestingWithoutParams,
                 name: str,
                 order: Tuple[int, int],
                 repeat: int,
                 time_limit: int,
                 data: List[Any]):
        self.test: DynamicTestingWithoutParams = test
        self.name: str = name
        self.order: Tuple[int, int] = order
        self.repeat: int = repeat
        self.time_limit: int = time_limit
        self.data: Optional[List[Any]] = data
        self.args_list: Optional[List[List[Any]]] = None

    def extract_parametrized_data(self):
        pass

    def check_errors(self):
        if self.repeat <= 0:
            raise UnexpectedError(f'Dynamic test "{self.name}" '
                                  f'should not be repeated <= 1 times, found {self.repeat}')


def to_dynamic_testing(source: str, args: List[str],
                       input_funcs: List[DynamicInputFunction]) -> DynamicTesting:

    class InputFunctionHandler:
        def __init__(self, funcs: List[DynamicInputFunction]):
            self.input_funcs: List[DynamicInputFunction] = []
            for func in funcs:
                self.input_funcs += [
                    DynamicInputFunction(func.trigger_count, func.input_function)]

        def eject_next_input(self, curr_output: str) -> Optional[str]:
            if len(self.input_funcs) == 0:
                return None

            input_function = self.input_funcs[0]
            trigger_count = input_function.trigger_count
            if trigger_count > 0:
                input_function.trigger()

            next_func = input_function.input_function

            new_input: Optional[str]
            try:
                obj = next_func(curr_output)
                if isinstance(obj, str) or obj is None:
                    new_input = obj
                elif isinstance(obj, CheckResult):
                    if obj.is_correct:
                        raise TestPassed()
                    else:
                        raise WrongAnswer(obj.feedback)
                else:
                    raise UnexpectedError(
                        'Dynamic input should return ' +
                        f'str or CheckResult objects only. Found: {type(obj)}')
            except BaseException as ex:
                from hstest.stage_test import StageTest
                StageTest.curr_test_run.set_error_in_test(ex)
                return None

            if input_function.trigger_count == 0:
                self.input_funcs.pop(0)

            if new_input is not None:
                new_input = clean_text(new_input)

            return new_input

    def dynamic_testing_function() -> Optional[CheckResult]:
        program = TestedProgram(source)
        output: str = program.start(*args)

        handler = InputFunctionHandler(input_funcs)

        while not program.is_finished():
            stdin = handler.eject_next_input(output)
            if stdin is None:
                program.execute(None)
                break
            output = program.execute(stdin)

        return None

    return dynamic_testing_function


def search_dynamic_tests(obj: 'StageTest') -> List['TestCase']:
    from hstest.test_case import TestCase
    methods: List[DynamicTestElement] = obj._dynamic_methods.get(type(obj), [])

    for m in methods:
        m.extract_parametrized_data()
        m.check_errors()

    tests: List[TestCase] = []

    for dte in sorted(methods, key=lambda x: x.order):
        for i in range(dte.repeat):
            tests += [
                TestCase(
                    dynamic_testing=lambda fn=dte: fn.test(obj),
                    time_limit=dte.time_limit
                )
            ]

    return tests
