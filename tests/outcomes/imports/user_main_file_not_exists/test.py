import os
import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.common.reflection_utils import get_main
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class UnexpectedErrorUserMainFileNotExists(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = UnexpectedErrorUserMainFileNotExists(get_main('bad_file')).run_tests()

        self.assertIn(
            'Error in test #1\n\n'
                        
            f'File "tests{os.sep}outcomes{os.sep}imports{os.sep}'
            f'user_main_file_not_exists{os.sep}bad_file.py" '
            'not found. Check if you deleted it.\n\n'
            
            'ImportError: No module named tests.outcomes.imports.user_main_file_not_exists.bad_file',

            feedback
        )


if __name__ == '__main__':
    Test().test()
