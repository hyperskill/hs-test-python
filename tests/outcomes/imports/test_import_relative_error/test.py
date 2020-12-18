import unittest
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestImportRelativeError(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == '1036\n', '')


@unittest.skip('Relative imports doesn\'t work')
class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestImportRelativeError('main').run_tests()

        self.assertEqual(cleandoc(
            """
            Error in test #1

            Traceback (most recent call last):
              File "main.py", line 1, in <module>
                from .main22 import x
            ModuleNotFoundError: No module named 'tests.outcomes.imports.test_import_relative_error.main22'
            """), feedback)


if __name__ == '__main__':
    Test().test()
