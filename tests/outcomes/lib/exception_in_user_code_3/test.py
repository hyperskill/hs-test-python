import unittest
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class ExceptionInUserCodeTest3(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = ExceptionInUserCodeTest3(source='module.main').run_tests()

        self.assertEqual(cleandoc(
            """
            Exception in test #1

            Traceback (most recent call last):
              File "main.py", line 2, in <module>
                Coffee is ready!\"\"\", raise_error_here)
            NameError: name 'raise_error_here' is not defined
            """), feedback)


if __name__ == '__main__':
    Test().test()
