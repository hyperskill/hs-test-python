import unittest
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestImportAbsoluteErrorCircular(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == '107\n', '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestImportAbsoluteErrorCircular().run_tests()

        correct_feedback = cleandoc("""
            Error in test #1

            Cannot decide which file to run out of the following: "main.py", "main2.py"
            Write "if __name__ == '__main__'" in one of them to mark it as an entry point.
            """)

        self.assertEqual(correct_feedback, feedback)


if __name__ == '__main__':
    Test().test()
