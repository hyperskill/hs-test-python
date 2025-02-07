from typing import List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestCommandLineArgumentsFailedSecondTestDynamicTesting(UserErrorTest):
    contain = """
    Wrong answer in test #2

    Please find below the output of your program during this failed test.
    
    ---
    
    Arguments: -in 123 -out 234
    
    4
    -in
    123
    -out
    234
    """  # noqa: W293

    def test1(self):
        pr = TestedProgram("main")
        pr.start("-in", "123", "-out", "234")
        return CheckResult(False, "")

    def test2(self):
        pr2 = TestedProgram("main2")
        pr2.start("--second", "main")
        return CheckResult(True, "")

    def generate(self) -> List[TestCase]:
        return [
            TestCase(dynamic_testing=self.test2),
            TestCase(dynamic_testing=self.test1),
        ]
