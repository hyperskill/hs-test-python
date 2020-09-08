import unittest
import os
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestImportAbsoluteErrorCircular(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == '10\n', '')


class Test(unittest.TestCase):
    def test(self):
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = TestImportAbsoluteErrorCircular(file).run_tests()

        self.assertIn(cleandoc(
            """
            Exception in test #1

            Traceback (most recent call last):
              File "main.py", line 1, in <module>
                import main2
            AttributeError: partially initialized module 'main2' has no attribute 'x' (most likely due to a circular import)
            """), feedback)


if __name__ == '__main__':
    Test().test()
