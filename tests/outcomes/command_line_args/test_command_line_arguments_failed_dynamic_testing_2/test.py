from typing import List

from hstest.check_result import wrong
from hstest.test_case import TestCase
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestCommandLineArgumentsFailedDynamicTesting3(UserErrorTest):
    contain = """
    Wrong answer in test #1

    Arguments: -in 123 -out 234
    """

    def test1(self):
        pr = TestedProgram("main")
        pr.start("-in", "123", "-out", "234")
        return wrong("")

    def generate(self) -> List[TestCase]:
        return [TestCase(dynamic_testing=self.test1)]
