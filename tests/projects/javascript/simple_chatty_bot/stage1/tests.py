import re

from hstest.stage_test import *
from hstest.test_case import TestCase
from hstest.check_result import CheckResult

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
