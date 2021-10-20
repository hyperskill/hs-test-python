import unittest
from typing import Any

from hstest.check_result import CheckResult, correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.execution.main_module_executor import MainModuleExecutor
from hstest.testing.runner.async_dynamic_testing_runner import AsyncDynamicTestingRunner
from hstest.testing.tested_program import TestedProgram


class TestDynamicMethodProgramNotFinishedAfterTestButShutDown(StageTest):
    runner = AsyncDynamicTestingRunner(MainModuleExecutor)

    @dynamic_test
    def test(self):
        pr = TestedProgram('main')

        out1 = pr.start()
        if out1 != "Server started!\n":
            return wrong("")

        return None

    def check(self, reply: str, attach: Any) -> CheckResult:
        if "Server stopped!\n" in reply:
            return correct()
        return wrong('')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestDynamicMethodProgramNotFinishedAfterTestButShutDown().run_tests()
        self.assertNotEqual(status, 0)
        self.assertEqual(
            feedback,
            "Error in test #1\n" +
            "\n" +
            "Program ran out of input. You tried to read more than expected.\n" +
            "\n" +
            "Please find below the output of your program during this failed test.\n" +
            "\n" +
            "---\n" +
            "\n" +
            "Server started!" +
            "\nServer stopped!"
        )


if __name__ == '__main__':
    Test().test()
