import unittest
import os
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestImportRelativeErrorCircular(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == '10\n', '')


class Test(unittest.TestCase):
    def test(self):
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = TestImportRelativeErrorCircular(file).run_tests()

        self.assertIn(cleandoc(
            """
            Error in test #1

            Traceback (most recent call last):
              File "main.py", line 1, in <module>
                from .main2 import x
              File "main2.py", line 1, in <module>
                from .main import y
              File "main.py", line 1, in <module>
                from .main2 import x
            ImportError: cannot import name 'x' from partially initialized module 
            """), feedback)


if __name__ == '__main__':
    Test().test()
