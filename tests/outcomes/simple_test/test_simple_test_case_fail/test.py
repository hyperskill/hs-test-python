import unittest
from typing import List

from hstest.stage_test import StageTest
from hstest.test_case import SimpleTestCase, TestCase


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
        status, feedback = TesSimpleTestCaseFail('main').run_tests()

        self.assertTrue("Wrong answer in test #1" in feedback)
        self.assertTrue("Fatal error" not in feedback)

        self.assertNotEqual(status, 0)
