import unittest
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.common.reflection_utils import get_main
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestImportRelativeError2(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == '10\n', '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestImportRelativeError2(get_main()).run_tests()

        self.assertIn(cleandoc(
            """
            Error in test #1

            Traceback (most recent call last):
              File "main.py", line 1, in <module>
                from .main2 import y
            ImportError: cannot import name 'y' from 
            """), feedback)


if __name__ == '__main__':
    Test().test()
