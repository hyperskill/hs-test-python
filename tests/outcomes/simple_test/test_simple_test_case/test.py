from typing import List

from hstest.stage_test import StageTest
from hstest.test_case import SimpleTestCase, TestCase


class TesSimpleTestCase(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            SimpleTestCase(stdin="123", stdout="123\n123", feedback=""),
            SimpleTestCase(stdin="567", stdout="567\n567", feedback=""),
        ]
