import unittest
from typing import List

from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestEmptyEval(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestEmptyEval(source_name='main').run_tests()

        self.assertIn('Exception in test #1\n'
                         '\n'
                         'Traceback (most recent call last):\n'
                         '  File "main.py", line 2, in <module>\n'
                         '    print(eval(")"))\n'
                         '  File "<string>", line 1\n', feedback)

        self.assertIn('SyntaxError: ', feedback)

        self.assertIn('\n'
                      'Please find below the output of your program during this failed test.\n'
                      '\n'
                      '---\n'
                      '\n'
                      '123', feedback)

        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
