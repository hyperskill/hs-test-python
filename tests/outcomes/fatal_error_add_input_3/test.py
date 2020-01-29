import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class FatalErrorAddInput3(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=['12'], attach='1\n12\n'),
            TestCase(stdin=[lambda x: CheckResult.true()]),
            TestCase(stdin=[lambda x: CheckResult(x == '1\n', x + '56')]),
            TestCase(stdin=[lambda x: 78])
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = FatalErrorAddInput3(
            'tests.outcomes.fatal_error_add_input_3.program'
        ).run_tests()

        self.assertIn('Fatal error in test #4, please '
                      'send the report to support@hyperskill.org', feedback)

        self.assertIn('FatalErrorException: Dynamic input should return '
                      'str or CheckResult objects only. Found: <class \'int\'>', feedback)
        self.assertEqual(status, -1)
