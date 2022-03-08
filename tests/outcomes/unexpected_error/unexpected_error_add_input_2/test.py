import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class UnexpectedErrorAddInput2(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[(2, lambda x: f'{0/0}')])
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = UnexpectedErrorAddInput2(source_name='main').run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Unexpected error in test #1'
                        '\n\nWe have recorded this bug and will fix it soon.' in feedback)

        self.assertTrue('ZeroDivisionError: division by zero' in feedback)


if __name__ == '__main__':
    Test().test()
