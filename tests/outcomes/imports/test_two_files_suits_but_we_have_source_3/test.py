import unittest
from typing import Any, List

from hstest import CheckResult, StageTest, TestCase


class TestImportRelativeError2(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == 'main2\n', '')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestImportRelativeError2('main2').run_tests()
        self.assertEqual("test OK", feedback)


if __name__ == '__main__':
    Test().test()
