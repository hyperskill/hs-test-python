from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.execution.main_module_executor import MainModuleExecutor
from hstest.testing.runner.async_dynamic_testing_runner import \
    AsyncDynamicTestingRunner
from hstest.testing.unittest.user_error_test import UserErrorTest


class FeedbackOnExceptionTest5(UserErrorTest):
    contain = """
            Exception in test #1
            
            Base ex raised
            
            Traceback (most recent call last):
              File "main.py", line 1, in <module>
                raise ZeroDivisionError()
            ZeroDivisionError"""  # noqa: W293

    runner = AsyncDynamicTestingRunner(MainModuleExecutor)

    def generate(self) -> List[TestCase]:
        return [
            TestCase(
                feedback_on_exception={
                    AttributeError: "Attribute Error raised!",
                    Exception: "Base ex raised",
                }
            )
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, "")
