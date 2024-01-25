from __future__ import annotations

import typing
from typing import Any

from hstest.common.utils import clean_text
from hstest.exception.outcomes import TestPassed, UnexpectedError, WrongAnswer
from hstest.testing.tested_program import TestedProgram

if typing.TYPE_CHECKING:
    from collections.abc import Callable

    from hstest import CheckResult, StageTest, TestCase
    from hstest.dynamic.input.dynamic_input_func import DynamicInputFunction

    DynamicTesting = Callable[[], CheckResult | None]
    DynamicTestingWithoutParams = Callable[[StageTest, Any], CheckResult | None]


class DynamicTestElement:
    def __init__(
        self,
        test: DynamicTestingWithoutParams,
        name: str,
        order: tuple[int, int],
        repeat: int,
        time_limit: int,
        feedback: str,
        data: list[Any],
        files: dict[str, str],
    ) -> None:
        self.test: DynamicTestingWithoutParams = test
        self.name: str = f'Data passed to dynamic method "{name}"'
        self.method_name = name
        self.order: tuple[int, int] = order
        self.repeat: int = repeat
        self.time_limit: int = time_limit
        self.feedback: str = feedback
        self.data: list[Any] | None = data
        self.files: dict[str, str] | None = files
        self.args_list: list[list[Any]] | None = None

    def extract_parametrized_data(self) -> None:
        if self.data is None:
            self.data = [[]]

        if type(self.data) not in {list, tuple}:
            msg = f"{self.name} should be of type " f'"list" or "tuple", found {type(self.data)}.'
            raise UnexpectedError(msg)

        if len(self.data) == 0:
            msg = f"{self.name} should not be empty."
            raise UnexpectedError(msg)

        found_lists_inside = True
        for obj in self.data:
            if type(obj) not in {list, tuple}:
                found_lists_inside = False
                break

        if found_lists_inside:
            self.args_list = self.data
        else:
            self.args_list = [[obj] for obj in self.data]

    def check_errors(self) -> None:
        if self.repeat < 0:
            msg = (
                f'Dynamic test "{self.method_name}" '
                f"should not be repeated < 0 times, found {self.repeat}"
            )
            raise UnexpectedError(msg)

        if self.files is not None:
            if type(self.files) != dict:
                msg = (
                    f"'Files' parameter in dynamic test should be of type "
                    f'"dict", found {type(self.files)}.'
                )
                raise UnexpectedError(msg)

            for k, v in self.files.items():
                if type(k) != str:
                    msg = (
                        f"All keys in 'files' parameter in dynamic test should be "
                        f'of type "str", found {type(k)}.'
                    )
                    raise UnexpectedError(msg)
                if type(v) != str:
                    msg = (
                        f"All values in 'files' parameter in dynamic test should be "
                        f'of type "str", found {type(v)}.'
                    )
                    raise UnexpectedError(msg)

    def get_tests(self, obj) -> list[DynamicTesting]:
        tests = []
        for _i in range(self.repeat):
            for args in self.args_list:
                tests += [lambda o=obj, a=args: self.test(o, *a)]
        return tests


def to_dynamic_testing(
    source: str, args: list[str], input_funcs: list[DynamicInputFunction]
) -> DynamicTesting:
    from hstest.dynamic.input.dynamic_input_func import DynamicInputFunction
    from hstest.test_case.check_result import CheckResult

    class InputFunctionHandler:
        def __init__(self, funcs: list[DynamicInputFunction]) -> None:
            self.input_funcs: list[DynamicInputFunction] = []
            for func in funcs:
                self.input_funcs += [DynamicInputFunction(func.trigger_count, func.input_function)]

        def eject_next_input(self, curr_output: str) -> str | None:
            if len(self.input_funcs) == 0:
                return None

            input_function = self.input_funcs[0]
            trigger_count = input_function.trigger_count
            if trigger_count > 0:
                input_function.trigger()

            next_func = input_function.input_function

            new_input: str | None
            try:
                obj = next_func(curr_output)
                if isinstance(obj, str) or obj is None:
                    new_input = obj
                elif isinstance(obj, CheckResult):
                    if obj.is_correct:
                        raise TestPassed
                    else:
                        raise WrongAnswer(obj.feedback)
                else:
                    raise UnexpectedError(
                        "Dynamic input should return "
                        + f"str or CheckResult objects only. Found: {type(obj)}"
                    )
            except BaseException as ex:
                from hstest.stage_test import StageTest

                StageTest.curr_test_run.set_error_in_test(ex)
                return None

            if input_function.trigger_count == 0:
                self.input_funcs.pop(0)

            if new_input is not None:
                new_input = clean_text(new_input)

            return new_input

    def dynamic_testing_function() -> CheckResult | None:
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


def search_dynamic_tests(obj: StageTest) -> list[TestCase]:
    from hstest.test_case.test_case import TestCase

    methods: list[DynamicTestElement] = obj.dynamic_methods()

    for m in methods:
        m.extract_parametrized_data()
        m.check_errors()

    tests: list[TestCase] = []

    for dte in sorted(methods, key=lambda x: x.order):
        for test in dte.get_tests(obj):
            tests += [
                TestCase(
                    dynamic_testing=test,
                    time_limit=dte.time_limit,
                    feedback=dte.feedback,
                    files=dte.files,
                )
            ]

    return tests
