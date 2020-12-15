import unittest
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.common.reflection_utils import get_main
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestImportAbsoluteErrorCircular(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == '10\n', '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestImportAbsoluteErrorCircular(get_main()).run_tests()

        correct_feedback = cleandoc("""
            Exception in test #1

            Traceback (most recent call last):
              File "main.py", line 1, in <module>
                import main2
              File "main2.py", line 1, in <module>
                import main
              File "main.py", line 2, in <module>
                print(main2.x)
            AttributeError: partially initialized module 'main2' has no attribute 'x' (most likely due to a circular import)
            """)

        self.assertEqual(correct_feedback, feedback)


if __name__ == '__main__':
    Test().test()
