import unittest
from typing import List, Any

from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest import CheckResult


class TestOutputWithStderrAndWithStdout(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase()
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.wrong('')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestOutputWithStderrAndWithStdout('main').run_tests()
        self.assertNotIn("stderr:", feedback)
        self.assertNotIn("stdout:", feedback)
        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
