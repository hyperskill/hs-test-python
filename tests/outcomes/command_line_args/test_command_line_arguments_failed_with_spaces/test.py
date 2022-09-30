from typing import List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestCommandLineArgumentsFailedWithSpaces(UserErrorTest):
    contain = """
    Wrong answer in test #1

    See arguments below:
    
    Please find below the output of your program during this failed test.
    
    ---
    
    Arguments: -spaces "some argument with spaces" -number 234 -onlySpaces "      "
    
    6
    -spaces
    some argument with spaces
    -number
    234
    -onlySpaces
    """  # noqa: W293

    def test(self):
        pr = TestedProgram('main')
        pr.start("-spaces", "some argument with spaces",
                 "-number", "234", "-onlySpaces", "      ")
        return CheckResult(False, "See arguments below:")

    def generate(self) -> List[TestCase]:
        return [
            TestCase(dynamic_testing=self.test)
        ]
