import os
import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase, SimpleTestCase


class TestSyntaxError1(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSyntaxError1(
            'tests.outcomes.test_syntax_error_1.program'
        ).run_tests()

        self.assertEqual('File "tests' + os.sep +
                            'outcomes' + os.sep +
                            'test_syntax_error_1' + os.sep + 'program.py", line 1\n'
                         'print\n'
                         'SyntaxError: unmatched \')\'', feedback)
        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
