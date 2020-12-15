import unittest
from typing import List

from hstest.common.reflection_utils import get_main
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
        status, feedback = TesSimpleTestCaseFail(get_main()).run_tests()

        self.assertTrue("Wrong answer in test #1" in feedback)
        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
