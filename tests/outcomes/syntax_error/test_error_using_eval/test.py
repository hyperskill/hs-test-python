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

        self.assertEqual('Exception in test #1\n'
                         '\n'
                         'Traceback (most recent call last):\n'
                         '  File "main.py", line 1, in <module>\n'
                         '    print(eval(")"))\n'
                         '  File "<string>", line 1\n'
                         '    )\n'
                         '    ^\n'
                         'SyntaxError: unmatched \')\'', feedback)
        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
