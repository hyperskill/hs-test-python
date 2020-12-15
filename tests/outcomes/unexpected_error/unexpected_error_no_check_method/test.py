import unittest
from typing import List

from hstest.common.reflection_utils import get_main
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class UnexpectedErrorNotGeneratingTests(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]


class Test(unittest.TestCase):
    def test(self):
        status, feedback = UnexpectedErrorNotGeneratingTests(get_main()).run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Unexpected error in test #1'
                        '\n\nWe have recorded this bug and will fix it soon.' in feedback)

        self.assertTrue('Can\'t check result: override "check" method' in feedback)
