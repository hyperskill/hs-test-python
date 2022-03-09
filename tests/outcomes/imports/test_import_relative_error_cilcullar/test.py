import unittest
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestImportRelativeErrorCircular(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == '1038\n', '')


@unittest.skip('Relative imports doesn\'t work')
class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestImportRelativeErrorCircular().run_tests()

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
