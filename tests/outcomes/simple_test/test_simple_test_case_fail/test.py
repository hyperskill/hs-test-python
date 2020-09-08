import unittest
import os
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase, SimpleTestCase


class TesSimpleTestCaseFail(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            SimpleTestCase(stdin="123",
                           stdout="123\n123",
                           feedback="You should output a number twice"),
            SimpleTestCase(stdin="567",
                           stdout="567\n567",
                           feedback="You should output this number twice")
        ]


class Test(unittest.TestCase):
    def test(self):
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = TesSimpleTestCaseFail(file).run_tests()

        self.assertTrue("Wrong answer in test #1" in feedback)
        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
