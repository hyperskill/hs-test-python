from typing import List

from hstest.stage_test import *
from hstest.test_case import TestCase, CheckResult

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class ChattyBotTest(StageTest):
    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin="John\n1\n2\n1", attach=("John", 22)),
            TestCase(stdin="Nick\n2\n0\n0", attach=("Nick", 35))
        ]

    def check(self, reply: str, clue: Any) -> CheckResult:
        lines = reply.strip().splitlines()
        if len(lines) != 7:
            return CheckResult.wrong(
                "You should output 7 lines!\n" +
                f"Lines found: {len(lines)}"
                f"Your output:\n"
                f"{reply.strip()}"
            )

        line_with_name = lines[3].lower()
        name = clue[0].lower()

        if name not in line_with_name:
            return CheckResult.wrong(
                "The name was " + clue[0] + "\n" +
                "But the 4-th line was:\n" +
                "\"" + lines[3] + "\"\n\n" +
                "4-th line should contain a name of the user"
            )

        line_with_age = lines[6].lower()
        age = str(clue[1])

        if age not in line_with_age:
            return CheckResult.wrong(
                "Can't find a correct age " +
                "in the last line of output! " +
                "Maybe you calculated the age wrong?\n\n" +
                "Your last line: \n" + "\"" + lines[6] + "\""
            )

        return CheckResult.correct()
