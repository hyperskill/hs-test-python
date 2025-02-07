from typing import Any

from hstest.check_result import CheckResult, correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.execution.main_module_executor import MainModuleExecutor
from hstest.testing.runner.async_dynamic_testing_runner import \
    AsyncDynamicTestingRunner
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestDynamicMethodProgramNotFinishedAfterTestButShutDown(UserErrorTest):
    contain = """
    Error in test #1

    Program ran out of input. You tried to read more than expected.
    
    Please find below the output of your program during this failed test.
    
    ---
    
    Server started!
    Server stopped!
    """  # noqa: W293

    runner = AsyncDynamicTestingRunner(MainModuleExecutor)

    @dynamic_test
    def test(self):
        pr = TestedProgram("main")

        out1 = pr.start()
        if out1 != "Server started!\n":
            return wrong("")

        return None

    def check(self, reply: str, attach: Any) -> CheckResult:
        if "Server stopped!\n" in reply:
            return correct()
        return wrong("")
