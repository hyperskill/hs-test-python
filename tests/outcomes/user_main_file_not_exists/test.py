import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class FatalErrorUserMainFileNotExists(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = FatalErrorUserMainFileNotExists(
            'tests.outcomes.fatal_error_user_main_file_not_exists.program'
        ).run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Fatal error in test #1, please '
                        'send the report to support@hyperskill.org' in feedback)

        self.assertTrue('ImportError: Error while finding module specification for '
                        '\'tests.outcomes.fatal_error_user_main_file_not_exists.program\' '
                        '(ModuleNotFoundError: No module named \'tests.outcomes.fatal_error'
                        '_user_main_file_not_exists\')' in feedback)
