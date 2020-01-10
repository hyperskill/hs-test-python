import unittest
from typing import List

from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class FatalErrorNotGeneratingTests(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]


class Test(unittest.TestCase):
    def test(self):
        status, feedback = FatalErrorNotGeneratingTests(
            'tests.outcomes.fatal_error_no_check_method.program'
        ).run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Fatal error in test #1, please '
                        'send the report to support@hyperskill.org' in feedback)

        self.assertTrue('Can\'t check result: override "check" method' in feedback)
