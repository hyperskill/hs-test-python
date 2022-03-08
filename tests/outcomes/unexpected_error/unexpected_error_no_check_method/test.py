import unittest
from typing import List

from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class UnexpectedErrorNotGeneratingTests(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]


class Test(unittest.TestCase):
    def test(self):
        status, feedback = UnexpectedErrorNotGeneratingTests(source_name='main').run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Unexpected error in test #1'
                        '\n\nWe have recorded this bug and will fix it soon.' in feedback)

        self.assertTrue('Can\'t check result: override "check" method' in feedback)


if __name__ == '__main__':
    Test().test()
