from __future__ import annotations

from typing import Any, TYPE_CHECKING, Union

from hstest.dynamic.input.dynamic_input_func import DynamicInputFunction
from hstest.dynamic.input.dynamic_testing import to_dynamic_testing
from hstest.exception.outcomes import UnexpectedError
from hstest.test_case.check_result import CheckResult

if TYPE_CHECKING:
    from collections.abc import Callable

    from hstest.dynamic.input.dynamic_input_func import InputFunction
    from hstest.dynamic.input.dynamic_testing import DynamicTesting

    SimpleStepikTest = str
    AdvancedStepikTest = tuple[str, Any]
    StepikTest = Union[SimpleStepikTest, AdvancedStepikTest]

    CheckFunction = Callable[[str, Any], CheckResult]

    PredefinedInput = str
    RuntimeEvaluatedInput = Union[
        PredefinedInput, InputFunction, tuple[int, InputFunction], DynamicInputFunction
    ]
    DynamicInput = Union[PredefinedInput, list[RuntimeEvaluatedInput]]

DEFAULT_TIME_LIMIT: int = 15000


class TestCase:
    def __init__(
        self,
        *,
        stdin: DynamicInput = "",
        args: list[str] | None = None,
        attach: Any = None,
        feedback: str = "",
        files: dict[str, str] | None = None,
        time_limit: int = DEFAULT_TIME_LIMIT,
        check_function: CheckFunction = None,
        feedback_on_exception: dict[type[Exception], str] | None = None,
        copy_to_attach: bool = False,
        dynamic_testing: DynamicTesting = None,
    ) -> None:
        self.source_name = None

        self.input: str | None = None
        self.args: list[str] = [] if args is None else args
        self.attach: Any = attach
        self.feedback = feedback
        self.files: dict[str, str] = {} if files is None else files
        self.time_limit: int = time_limit
        self.check_func: CheckFunction = check_function
        self.feedback_on_exception: dict[type[Exception], str] = (
            {} if feedback_on_exception is None else feedback_on_exception
        )
        self.input_funcs = []

        self._dynamic_testing: DynamicTesting = dynamic_testing

        if dynamic_testing is not None:
            return

        if copy_to_attach:
            if attach is not None:
                msg = "Attach is not None " "but copying from stdin is specified"
                raise UnexpectedError(msg)
            if type(stdin) != str:
                msg = (
                    "To copy stdin to attach stdin should be of type str "
                    f"but found type {type(stdin)}"
                )
                raise UnexpectedError(msg)
            self.attach = stdin

        if type(stdin) == str:
            self.input = stdin
            self.input_funcs = [DynamicInputFunction(1, lambda x: stdin)]
        else:
            if type(stdin) != list:
                msg = (
                    "Stdin should be either of type str or list "
                    f"but found type {type(stdin)}"
                )
                raise UnexpectedError(msg)
            for elem in stdin:  # type: RuntimeEvaluatedInput
                if type(elem) == DynamicInputFunction:
                    self.input_funcs += [elem]

                elif type(elem) == str:
                    self.input_funcs += [
                        DynamicInputFunction(1, lambda x, inp=elem: inp)
                    ]

                elif str(type(elem)) in {"<class 'function'>", "<class 'method'>"}:
                    self.input_funcs += [DynamicInputFunction(1, elem)]

                elif type(elem) in {tuple, list}:
                    if len(elem) == 2:
                        trigger_count: int = elem[0]
                        input_function: InputFunction = elem[1]

                        if type(trigger_count) != int:
                            msg = (
                                f"Stdin element's 1st element should be of type int, "
                                f"found {type(trigger_count)}"
                            )
                            raise UnexpectedError(msg)

                        if str(type(input_function)) not in {
                            "<class 'function'>",
                            "<class 'method'>",
                        }:
                            msg = (
                                f"Stdin element's 2nd element should be of type function, "
                                f"found {type(input_function)}"
                            )
                            raise UnexpectedError(msg)

                        self.input_funcs += [
                            DynamicInputFunction(trigger_count, input_function)
                        ]
                    else:
                        msg = f"Stdin element should have size 2, found {len(elem)}"
                        raise UnexpectedError(msg)

                else:
                    msg = (
                        f"Stdin element should have type DynamicInputFunction or "
                        f"tuple of size 1 or 2, found element of type {type(elem)}"
                    )
                    raise UnexpectedError(msg)

    @property
    def dynamic_testing(self) -> DynamicTesting:
        if self._dynamic_testing is None:
            self._dynamic_testing = to_dynamic_testing(
                self.source_name, self.args, self.input_funcs
            )
        return self._dynamic_testing

    @staticmethod
    def from_stepik(stepik_tests: list[StepikTest]) -> list[TestCase]:
        hs_tests = []
        for test in stepik_tests:
            if type(test) in {list, tuple}:
                hs_test = TestCase(stdin=test[0], attach=test[1])
            elif type(test) is str:
                hs_test = TestCase(stdin=test)
            else:
                raise UnexpectedError("Bad test: " + str(test))
            hs_tests += [hs_test]
        return hs_tests


class SimpleTestCase(TestCase):
    def __init__(self, *, stdin: str, stdout: str, feedback: str, **kwargs) -> None:
        super().__init__(stdin=stdin, attach=stdout, feedback=feedback, **kwargs)
        self.check_func = self._custom_check

    def _custom_check(self, reply: str, expected: str):
        is_correct = reply.strip() == expected.strip()
        return CheckResult(is_correct, "")
