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
        status, feedback = TestOutputWithStderrAndWithStdout().run_tests()
        self.assertIn("Wrong answer in test #1\n\n"
                      "Please find below the output of your program during this failed test."
                      "\n\n---\n\n"
                      "stdout:\nUser stdout output!\nUser stdout output!\nUser stdout output!\n\n"
                      "stderr:\nUser stderr output!\nUser stderr output!\nUser stderr output!", feedback)
        self.assertNotEqual(status, 0)


if __name__ == '__main__':
    Test().test()
