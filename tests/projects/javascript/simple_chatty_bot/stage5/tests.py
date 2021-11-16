import unittest

from hstest.stage_test import *
from hstest.test_case import TestCase

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class ChattyBotTest(StageTest):
    def generate(self) -> List[TestCase]:
        stdin = "Marry\n1\n0\n5\n10"
        for i in range(10):
            stdin += f'\n{i}'
        return [
            TestCase(stdin=stdin, attach=("Marry", 40, 10))
        ]

    def check(self, reply: str, clue: Any) -> CheckResult:
        lines = reply.strip().splitlines()
        length = 9 + clue[2] + 1
        if len(lines) <= length:
            return CheckResult.wrong(
                f"You should output at least {length} lines " +
                f"(for the count number {clue[2]}).\n" +
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
                "Can't find a correct age! " +
                "Maybe you calculated the age wrong?\n\n" +
                "Your line with age: \n" + "\"" + lines[6] + "\""
            )

        for i in range(clue[2] + 1):
            num_line = lines[i + 8].strip().replace(' ', '')
            actual_num = f'{i}!'

            if num_line != actual_num:
                return CheckResult.wrong(
                    f"Expected {i + 8}-th line: \n" +
                    f"\"{actual_num}\"\n" +
                    f"Your {i + 8}-th line: \n" +
                    f"\"{num_line}\""
                )

        last_line = lines[-1]
        if "Congratulations, have a nice day!" != last_line:
            return CheckResult.wrong(
                "Your last line should be:\n" +
                "\"Congratulations, have a nice day!\"\n" +
                "Found:\n" +
                f"\"{last_line}\""
            )

        return CheckResult.correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = ChattyBotTest().run_tests()
        self.assertEqual(status, 0)
        self.assertEqual(feedback, 'test OK')


if __name__ == '__main__':
    Test().test()
