from typing import List, Dict, Any, Tuple, Callable, Union, Optional
from hstest.check_result import CheckResult
from hstest.dynamic.stdin import DynamicInputFunction, InputFunction
from hstest.exceptions import FatalErrorException

SimpleStepikTest = str
AdvancedStepikTest = Tuple[str, Any]
StepikTest = Union[SimpleStepikTest, AdvancedStepikTest]

CheckFunction = Callable[[str, Any], CheckResult]

PredefinedInput = str
RuntimeEvaluatedInput = Union[
    PredefinedInput, InputFunction, Tuple[int, InputFunction], DynamicInputFunction]
DynamicInput = Union[PredefinedInput, List[RuntimeEvaluatedInput]]


class TestCase:
    def __init__(self, *,
                 stdin: DynamicInput = '',
                 args: List[str] = None,
                 attach: Any = None,
                 files: Dict[str, str] = None,
                 time_limit: int = 15000,
                 check_function: CheckFunction = None,
                 feedback_on_exception: Dict[type, str] = None,
                 copy_to_attach=False,
                 ):
        self.input: Optional[str] = None
        self.args: List[str] = [] if args is None else args
        self.attach: Any = attach
        self.files: Dict[str, str] = {} if files is None else files
        self.time_limit: int = time_limit
        self.check_function: CheckFunction = check_function
        self.feedback_on_exception: Dict[type, str] = (
            {} if feedback_on_exception is None else feedback_on_exception)
        self.input_funcs = []

        if copy_to_attach:
            if attach is not None:
                raise FatalErrorException(
                    'Attach is not None '
                    'but copying from stdin is specified')
            if type(stdin) != str:
                raise FatalErrorException(
                    'To copy stdin to attach stdin should be of type str '
                    f'but found type {type(stdin)}')
            self.attach = stdin

        if type(stdin) == str:
            self.input = stdin
            self.input_funcs = [DynamicInputFunction(1, lambda x: stdin)]
        else:
            if type(stdin) != list:
                raise FatalErrorException(
                    'Stdin should be either of type str ot list '
                    f'but found type {type(stdin)}')
            for elem in stdin:  # type: RuntimeEvaluatedInput
                if type(elem) == DynamicInputFunction:
                    self.input_funcs += [elem]

                elif type(elem) == str:
                    self.input_funcs += [DynamicInputFunction(1, lambda x: elem)]

                elif str(type(elem)) == "<class 'function'>":
                    self.input_funcs += [DynamicInputFunction(1, elem)]

                elif type(elem) in (tuple, list):
                    if len(elem) == 2:
                        self.input_funcs += [DynamicInputFunction(*elem)]
                    else:
                        raise FatalErrorException(
                            f'Stdin element should have size 2, found {len(elem)}')

                else:
                    raise FatalErrorException(
                        f'Stdin element should have type DynamicInputFunction or '
                        f'tuple of size 1 or 2, found element of type {type(elem)}')

    @staticmethod
    def from_stepik(stepik_tests: List[StepikTest]) -> List['TestCase']:
        hs_tests = []
        for test in stepik_tests:
            hs_test = TestCase()
            if type(test) in (list, tuple):
                hs_test.input = test[0]
                hs_test.attach = test[1]
            elif type(test) is str:
                hs_test.input = test
            else:
                raise ValueError("Bad test: " + str(test))
            hs_tests += [hs_test]
        return hs_tests


class SimpleTestCase(TestCase):
    def __init__(self, *, stdin: str, stdout: str, feedback: str, **kwargs):
        super().__init__(stdin=stdin, **kwargs)
        self.stdout = stdout
        self.feedback = feedback
        self.check_function = self._custom_check

    def _custom_check(self, reply: str, expected: str):
        is_correct = reply.strip() == expected.strip()
        return CheckResult(is_correct, self.feedback)
