import os
from inspect import cleandoc
import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase, SimpleTestCase


class TestSyntaxError2(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]


class Test(unittest.TestCase):
    def test(self):
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = TestSyntaxError2(file).run_tests()

        self.assertEqual('File "tests' + os.sep +
                            'outcomes' + os.sep + 'syntax_error' + os.sep +
                            'test_syntax_error_2' + os.sep + 'main.py", line 1\n'           
                         'print(12 \n'
                         'SyntaxError: invalid syntax', feedback)
        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
