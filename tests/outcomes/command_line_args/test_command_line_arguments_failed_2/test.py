import unittest
from typing import Any, List

from hstest.check_result import CheckResult, wrong
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestCommandLineArgumentsFailed2(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(args=["-in", "123", "-out", "234"])
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return wrong("")


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestCommandLineArgumentsFailed2('main').run_tests()
        self.assertNotEqual(status, 0)

        self.assertEqual(
            feedback,
            "Wrong answer in test #1\n" +
            "\n" +
            "Arguments: -in 123 -out 234"
        )


if __name__ == '__main__':
    Test().test()
