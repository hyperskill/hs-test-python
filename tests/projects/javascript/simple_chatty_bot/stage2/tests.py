from typing import List

from hstest.stage_test import *
from hstest.test_case import TestCase
from hstest.check_result import CheckResult

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class ChattyBotTest(StageTest):
    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin="John", attach="John"),
            TestCase(stdin="Nick", attach="Nick")
        ]

    def check(self, reply: str, clue: Any) -> CheckResult:
        lines = reply.strip().splitlines()
        if len(lines) != 4:
            return CheckResult.wrong(
                "You should output 4 lines!\n" +
                f"Lines found: {len(lines)}"
                f"Your output:\n"
                f"{reply.strip()}"
            )

        line_with_name = lines[3].lower()
        name = clue.lower()

        if name not in line_with_name:
            return CheckResult.wrong(
                "The name was " + clue + "\n" +
                "But the 4-th line was:\n" +
                "\"" + lines[3] + "\"\n\n" +
                "4-th line should contain a name of the user"
            )

        return CheckResult.correct()
