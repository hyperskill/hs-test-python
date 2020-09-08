import unittest
import os
from inspect import cleandoc
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase, SimpleTestCase


class TesSimpleTestCase(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            SimpleTestCase(stdin="123", stdout="123\n123", feedback=''),
            SimpleTestCase(stdin="567", stdout="567\n567", feedback='')
        ]


class Test(unittest.TestCase):
    def test(self):
        file = __file__.replace(os.sep, '.')[:-3]
        file = file[file.find('.tests.') + 1: file.rfind('.') + 1] + 'main'
        status, feedback = TesSimpleTestCase(file).run_tests()

        self.assertEqual('test OK', feedback)
        self.assertEqual(status, 0)
