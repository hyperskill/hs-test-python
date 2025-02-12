from typing import List

from hstest.check_result import CheckResult
from hstest.stage_test import *
from hstest.test_case import TestCase

CheckResult.correct = lambda: CheckResult(True, "")
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class ChattyBotTest(StageTest):
    def generate(self) -> List[TestCase]:
        return [TestCase(stdin="Marry\n1\n0\n5\n10", attach=("Marry", 40, 10))]

    def check(self, reply: str, clue: Any) -> CheckResult:
        lines = reply.strip().splitlines()
        length = 9 + clue[2] + 1
        if len(lines) != length:
            return CheckResult.wrong(
                f"You should output {length} lines "
                + f"(for the count number {clue[2]}).\n"
                + f"Lines found: {len(lines)}\n"
                f"Your output:\n"
                f"{reply.strip()}"
            )

        line_with_name = lines[3].lower()
        name = clue[0].lower()

        if name not in line_with_name:
            return CheckResult.wrong(
                "The name was "
                + clue[0]
                + "\n"
                + "But the 4-th line was:\n"
                + '"'
                + lines[3]
                + '"\n\n'
                + "4-th line should contain a name of the user"
            )

        line_with_age = lines[6].lower()
        age = str(clue[1])

        if age not in line_with_age:
            return CheckResult.wrong(
                "Can't find a correct age "
                + "in the last line of output! "
                + "Maybe you calculated the age wrong?\n\n"
                + "Your last line: \n"
                + '"'
                + lines[6]
                + '"'
            )

        for i in range(clue[2] + 1):
            num_line = lines[i + 8].strip().replace(" ", "")
            actual_num = f"{i}!"

            if num_line != actual_num:
                return CheckResult.wrong(
                    f"Expected {i + 8}-th line: \n"
                    + f'"{actual_num}"\n'
                    + f"Your {i + 8}-th line: \n"
                    + f'"{num_line}"'
                )

        return CheckResult.correct()
