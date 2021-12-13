import re
import unittest

from hstest.stage_test import *
from hstest.test_case import TestCase

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class ChattyBotTest(StageTest):
    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, clue: Any) -> CheckResult:
        lines = reply.strip().splitlines()
        if len(lines) != 2:
            return CheckResult.wrong(
                "You should output exactly 2 lines!\n" +
                f"Lines found: {len(lines)}"
                f"Your output:\n"
                f"{reply.strip()}"
            )

        if not re.match(".*\\d.*", lines[1]):
            return CheckResult.wrong(
                "The second line should contain a year!\n" +
                "Your second line: \"" + lines[1] + "\""
            )

        return CheckResult.correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = ChattyBotTest().run_tests()
        self.assertEqual(status, 0)
        self.assertEqual(feedback, 'test OK')


if __name__ == '__main__':
    Test().test()
