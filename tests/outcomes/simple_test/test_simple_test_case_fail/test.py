from typing import List

from hstest.test_case import SimpleTestCase, TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TesSimpleTestCaseFail(UserErrorTest):
    contain = """
            Wrong answer in test #1

            You should output a number twice
            
            Please find below the output of your program during this failed test.
            Note that the '>' character indicates the beginning of the input line.
            
            ---
            
            > 123
            123
            """  # noqa: W293

    def generate(self) -> List[TestCase]:
        return [
            SimpleTestCase(
                stdin="123",
                stdout="123\n123",
                feedback="You should output a number twice",
            ),
            SimpleTestCase(
                stdin="567",
                stdout="567\n567",
                feedback="You should output this number twice",
            ),
        ]
