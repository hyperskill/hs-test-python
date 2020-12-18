import unittest
from typing import Any

from hstest.check_result import CheckResult, correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestDynamicMethodProgramNotFinishedAfterTestButShutDown(StageTest):
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
        self.assertEqual(status, 0)
        self.assertEqual(
            feedback,
            "test OK"
        )


if __name__ == '__main__':
    Test().test()
