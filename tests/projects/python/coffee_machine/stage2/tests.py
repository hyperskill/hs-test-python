import unittest

from hstest.stage_test import *
from hstest.test_case import TestCase

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)

class CoffeeMachineTest(StageTest):
    def generate(self) -> List[TestCase]:
        return TestCase.from_stepik(
            [
                ('25', '25'),
                ('125', '125'),
                ('1', '1'),
                ('123', '123')
            ]
        )

    def check(self, reply: str, clue: Any) -> CheckResult:

        lines = reply.splitlines()

        if len(lines) < 3:
            return CheckResult.wrong(
                'Output contains less than 3 lines, '
                'but should output at least 3 lines')

        last_3_lines = reply.splitlines()[-3:]
        cups = int(clue)
        water = milk = beans = False
        for line in last_3_lines:
            line = line.lower()
            if 'milk' in line:
                milk = str(cups * 50) in line

                if not milk:
                    return CheckResult.wrong(
                        f"For the input {clue} your program output:\n\"" +
                        f"{line}\"\nbut the amount of milk should be {cups * 50}"
                    )

            elif 'water' in line:
                water = str(cups * 200) in line

                if not water:
                    return CheckResult.wrong(
                        f"For the input {clue} your program output:\n" +
                        f"{line}\nbut the amount of water should be {cups * 200}"
                    )

            elif 'beans' in line:
                beans = str(cups * 15) in line

                if not beans:
                    return CheckResult.wrong(
                        f"For the input {clue} your program output:\n" +
                        f"{line}\nbut the amount of beans should be {cups * 15}"
                    )

            else:
                return CheckResult.wrong(
                    "One of the last 3 lines " +
                    "doesn't contain \"milk\", \"water\" or \"beans\""
                )

        if not water:
            return CheckResult.wrong("There is no line with amount of water")

        if not milk:
            return CheckResult.wrong("There is no line with amount of milk")

        if not beans:
            return CheckResult.wrong("There is no line with amount of coffee beans")

        return CheckResult.correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = CoffeeMachineTest().run_tests()
        self.assertEqual(status, 0)
        self.assertEqual(feedback, 'test OK')


if __name__ == '__main__':
    Test().test()

