import unittest
import os
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class SuccessTest(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin='2\n4', attach='6\n'),
            TestCase(stdin='1\n3', attach='4\n'),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == attach, '')


class Test(unittest.TestCase):
    def test(self):
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'folder.main'
        status, feedback = SuccessTest(file).run_tests()
        self.assertEqual(status, 0)
        self.assertEqual(feedback, 'test OK')


if __name__ == '__main__':
    Test().test()
