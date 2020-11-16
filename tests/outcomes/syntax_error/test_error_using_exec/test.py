import os
from inspect import cleandoc
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
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = TestSyntaxError1(file).run_tests()

        self.assertEqual('Traceback (most recent call last):\n'
                         '  File "main.py", line 1, in <module>\n'
                         '    exec("print)")\n'
                         '  File "<string>", line 1\n'
                         '    print)\n'
                         '         ^\n'
                         'SyntaxError: unmatched \')\'', feedback)
        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
