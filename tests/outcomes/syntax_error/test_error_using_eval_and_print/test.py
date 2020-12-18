import unittest
from typing import List

from hstest.common.reflection_utils import get_main
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestEmptyEval(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestEmptyEval(get_main()).run_tests()

        self.assertIn('Exception in test #1\n'
                         '\n'
                         'Traceback (most recent call last):\n'
                         '  File "main.py", line 2, in <module>\n'
                         '    print(eval(")"))\n'
                         '  File "<string>", line 1\n'
                         '    )\n'
                         '    ^\n'
                         'SyntaxError: '
                         , feedback)

        self.assertIn('\n'
                      'Please find below the output of your program during this failed test.\n'
                      '\n'
                      '---\n'
                      '\n'
                      '123', feedback)

        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
