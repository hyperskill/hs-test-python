from typing import List

from hstest.check_result import correct
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestDynamicMethodUnexpectedErrorNoCheckMethod(StageTest):

    @dynamic_test
    def test(self):
        return correct()

    def generate(self) -> List[TestCase]:
        return [TestCase(dynamic_testing=lambda: correct())]
