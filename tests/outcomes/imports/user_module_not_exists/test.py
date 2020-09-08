import unittest
from typing import Any, List
import os
from inspect import cleandoc

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class UnexpectedErrorUserModuleNotExists(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = UnexpectedErrorUserModuleNotExists('tests.bad_module').run_tests()

        self.assertIn(
            'Error in test #1\n\n'
                                    
            f'File "tests{os.sep}bad_module.py" '
            'not found. Check if you deleted it.\n\n'
            
            'ImportError: No module named tests.bad_module',

            feedback
        )


if __name__ == '__main__':
    Test().test()
