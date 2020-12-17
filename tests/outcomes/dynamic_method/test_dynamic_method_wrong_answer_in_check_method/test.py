import unittest
from typing import Any

from hstest.check_result import CheckResult, wrong
from hstest.common.reflection_utils import get_main
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.testing.tested_program import TestedProgram


class TestDynamicMethodUnexpectedErrorNoCheckMethod(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram(get_main())
        main.start()
        main.execute('main')
        main.execute("main2")
        return None

    def check(self, reply: str, attach: Any) -> CheckResult:
        return wrong("WA1")


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestDynamicMethodUnexpectedErrorNoCheckMethod().run_tests()
        self.assertNotEqual(status, 0)
        self.assertIn(
            "Wrong answer in test #1\n" +
            "\n" +
            "WA1",
            feedback
        )


if __name__ == '__main__':
    Test().test()
