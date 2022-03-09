import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class UnexpectedErrorAddInput3(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=['12'], attach='1\n12\n'),
            TestCase(stdin=[lambda x: CheckResult.correct()]),
            TestCase(stdin=[lambda x: CheckResult(x == '1\n', x + '56')]),
            TestCase(stdin=[lambda x: 78])
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = UnexpectedErrorAddInput3().run_tests()

        self.assertIn('Unexpected error in test #4'
                      '\n\nWe have recorded this bug and will fix it soon.', feedback)

        self.assertIn('UnexpectedError: Dynamic input should return '
                      'str or CheckResult objects only. Found: <class \'int\'>', feedback)
        self.assertEqual(status, -1)
