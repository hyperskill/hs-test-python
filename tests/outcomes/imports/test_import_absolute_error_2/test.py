import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class TestImportAbsoluteError2(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == '104\n', '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestImportAbsoluteError2(source_name='main').run_tests()
        self.assertEqual("test OK", feedback)


if __name__ == '__main__':
    Test().test()
