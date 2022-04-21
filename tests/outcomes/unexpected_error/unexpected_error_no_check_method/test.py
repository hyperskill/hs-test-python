from typing import List

from hstest.test_case import TestCase
from testing.unittest.unexepected_error_test import UnexpectedErrorTest


class UnexpectedErrorNotGeneratingTests(UnexpectedErrorTest):
    contain = [
        """
        Unexpected error in test #1

        We have recorded this bug and will fix it soon.
        """,
        "Can't check result: override \"check\" method"
    ]

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]
