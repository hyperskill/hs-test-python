import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.common.reflection_utils import get_main
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestCommandLineArgumentsFailedSecondTest(StageTest):
    def generate(self) -> List[TestCase]:
        return [
            TestCase(args=["-in", "123", "-out", "234"], attach=True),
            TestCase(args=["-in", "123", "-out", "234"], attach=False),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(attach, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCommandLineArgumentsFailedSecondTest(get_main()).run_tests()
        self.assertNotEqual(status, 0)

        self.assertEqual(
            feedback,
            "Wrong answer in test #2\n" +
            "\n" +
            "Arguments: -in 123 -out 234"
        )


if __name__ == '__main__':
    Test().test()
