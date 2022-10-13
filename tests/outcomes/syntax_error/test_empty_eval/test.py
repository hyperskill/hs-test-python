from typing import List

from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestEmptyEval(UserErrorTest):
    contain = [
        """
        Exception in test #1

        Traceback (most recent call last):
          File "main.py", line 1, in <module>
            print(eval(""))
          File "<string>", line 0""",
        "SyntaxError: "
    ]

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]
