from typing import List

from hstest.check_result import wrong
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestDynamicInputFailInfiniteLoop(UserErrorTest):
    contain = """
    Wrong answer in test #1

    Wrong
    """

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=[lambda x: wrong("Wrong")])
        ]
