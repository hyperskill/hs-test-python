import unittest
from typing import List

from hstest.common.reflection_utils import get_main
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
        status, feedback = TesSimpleTestCase(get_main()).run_tests()
        self.assertEqual('test OK', feedback)
        self.assertEqual(status, 0)
