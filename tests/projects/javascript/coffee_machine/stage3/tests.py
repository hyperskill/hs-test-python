import unittest

from hstest.stage_test import *
from hstest.test_case import TestCase

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class CoffeeMachineTest(StageTest):
    def generate(self) -> List[TestCase]:
        return TestCase.from_stepik(
            [
                ('300\n65\n111\n1\n', (True, 0, True)),
                ('600\n153\n100\n1', (True, 2, True)),
                ('1400\n150\n100\n1', (True, 2, True)),
                ('1400\n1500\n45\n1', (True, 2, True)),
                ('599\n250\n200\n10', (False, 2, True)),
                ('34564\n43423\n23234\n1', (True, 171, True)),
                ('345640\n434230\n23234\n1', (True, 1547, True)),
                ('345640\n43423\n23234\n19246', (False, 868, True)),

                ('399\n112\n111\n1', (True, 0, False)),
                ('2400\n249\n100\n1', (True, 3, False)),
                ('1400\n1500\n44\n1', (True, 1, False)),
                ('500\n250\n200\n10', (False, 2, False)),
                ('600\n250\n200\n10', (False, 3, False)),
                ('345640\n43423\n23234\n1', (True, 867, False)),
                ('345640\n434230\n23234\n19246', (False, 1548, False)),
                ('34564\n43423\n23234\n19246', (False, 172, False)),
            ]
        )

    def check(self, reply: str, clue: Any) -> CheckResult:
        user_output = reply.split(':')[-1].strip()
        lowered_output = user_output.lower()
        print("----")
        print(lowered_output)
        print("----")
        ans, amount, show_tests = clue
        if ans:
            if amount > 0:
                is_correct = f'{amount}' in lowered_output and 'yes' in lowered_output
                if is_correct:
                    if f'{amount}.' in lowered_output:
                        return CheckResult.wrong(
                            "There is a dot after an amount of cups. "
                            "There should be no dot.\n"
                            "Your output:\n" +
                            user_output
                        )
                    return CheckResult.correct()

                else:
                    right_output = (
                        "Yes, I can make that amount of coffee" +
                        f" (and even {amount} more than that)"
                    )

                    if show_tests:
                        return CheckResult.wrong(
                            "Your output:\n" +
                            user_output +
                            "\nRight output:\n" +
                            right_output
                        )

                    else:
                        return CheckResult.wrong('')
            if 'yes, i can make that amount of coffee' == lowered_output:
                return CheckResult.correct()
            else:
                right_output = (
                    "Yes, I can make that amount of coffee"
                )

                if show_tests:
                    return CheckResult.wrong(
                        "Your output:\n" +
                        user_output +
                        "\nRight output:\n" +
                        right_output
                    )

                else:
                    return CheckResult.wrong('')

        else:
            cond1 = 'no' in lowered_output
            cond2 = str(amount) in lowered_output

            if cond1 and cond2:
                if f'{amount}.' in lowered_output:
                    return CheckResult.wrong(
                        "There is a dot after an amount of cups. "
                        "There should be no dot.\n"
                        "Your output:\n" +
                        user_output
                    )
                return CheckResult.correct()

            else:
                right_output = (
                    "No, I can make only " +
                    f"{amount} cup(s) of coffee"
                )

                if show_tests:
                    return CheckResult.wrong(
                        "Your output:\n" +
                        user_output +
                        "\nRight output:\n" +
                        right_output
                    )
                else:
                    return CheckResult.wrong('')


class Test(unittest.TestCase):
    def test(self):
        status, feedback = CoffeeMachineTest().run_tests()
        self.assertEqual(feedback, 'test OK')
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()

