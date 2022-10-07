from typing import List

from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestSyntaxError2(UserErrorTest):
    contain = [
        """
        Exception in test #1

        Traceback (most recent call last):
          File "main.py", line 1
            print(12 23)
        """,
        """
        SyntaxError: 
        """
    ]

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]
