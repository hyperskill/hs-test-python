import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class UnexpectedErrorEmptyTestCases(StageTest):

    def generate(self) -> List[TestCase]:
        return []

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = UnexpectedErrorEmptyTestCases(source_name='main').run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Unexpected error during testing'
                        '\n\nWe have recorded this bug and will fix it soon.' in feedback)

        self.assertTrue('No tests found' in feedback)


if __name__ == '__main__':
    Test().test()
