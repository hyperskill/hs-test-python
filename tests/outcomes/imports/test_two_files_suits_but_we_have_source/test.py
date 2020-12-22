import unittest
from inspect import cleandoc
from typing import Any, List

from hstest import CheckResult, StageTest, TestCase, correct


class TestImportRelativeError2(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestImportRelativeError2('main').run_tests()

        self.assertIn(cleandoc(
            """
            Error in test #1

            Cannot decide which file to run out of the following: "main1.py", "main2.py"
            Write "if __name__ == '__main__'" in one of them to mark it as an entry point.
            """), feedback)


if __name__ == '__main__':
    Test().test()
