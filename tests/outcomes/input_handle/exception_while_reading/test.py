import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class ExceptionWhileReading(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin='1'),
            TestCase(stdin='strange')
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = ExceptionWhileReading('main').run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Exception in test #2' in feedback)
        self.assertTrue('Traceback (most recent call last):' in feedback)
        self.assertTrue('    print(get_line())' in feedback)
        self.assertTrue('    return get_num()' in feedback)
        self.assertTrue('    return get()' in feedback)
        self.assertTrue('    return int(input())' in feedback)
        self.assertTrue('ValueError: invalid literal for '
                        'int() with base 10: \'strange\'' in feedback)
