import unittest
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestImportAbsoluteErrorCircular2(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == '105\n', '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestImportAbsoluteErrorCircular2('main').run_tests()

        correct_feedback = cleandoc("""
            Exception in test #1

            Traceback (most recent call last):
              File "main.py", line 1, in <module>
                import main2
              File "main2.py", line 1, in <module>
                import main
              File "main.py", line 2, in <module>
                print(main2.x)
            """)

        self.assertIn(correct_feedback, feedback)


if __name__ == '__main__':
    Test().test()
