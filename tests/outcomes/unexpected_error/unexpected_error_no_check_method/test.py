import unittest
import os
from inspect import cleandoc
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
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = FatalErrorNotGeneratingTests(file).run_tests()

        self.assertEqual(status, -1)
        self.assertTrue('Unexpected error in test #1'
                        '\n\nWe have recorded this bug and will fix it soon.' in feedback)

        self.assertTrue('Can\'t check result: override "check" method' in feedback)
