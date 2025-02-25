from typing import List

from hstest.stage_test import *
from hstest.test_case import TestCase
from hstest.check_result import CheckResult

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)

test1_input = '''remaining
buy
2
buy
2
fill
1000
0
0
0
buy
2
take
remaining
exit
'''

test2_input = '''remaining
fill
3000
3000
3000
3000
remaining
exit
'''

test3_input = '''remaining
buy
1
remaining
exit
'''

test4_input = '''remaining
buy
2
remaining
exit
'''

test5_input = '''remaining
buy
3
remaining
exit
'''

test6_input = '''remaining
take
remaining
exit
'''

test7_input = '''remaining
buy
back
remaining
exit
'''


class CoffeeMachineTest(StageTest):
    def generate(self) -> List[TestCase]:
        return TestCase.from_stepik(
            [
                (
                    test1_input,
                    (
                        700 - 400,
                        390 - 540,
                        80 - 120,
                        7 - 9,
                        0 - 550,
                        "This test is exactly like in the example "
                        "- try to run it by yourself"
                    )
                ),

                (
                    test2_input,
                    (
                        3000,
                        3000,
                        3000,
                        3000,
                        0,
                        "This test checks \"fill\" action"
                    )
                ),

                (
                    test3_input,
                    (
                        -250,
                        0,
                        -16,
                        -1,
                        4,
                        "This test checks \"buy\" " +
                        "action with the first variant of coffee"
                    )
                ),

                (
                    test4_input,
                    (
                        -350,
                        -75,
                        -20,
                        -1,
                        7,
                        "This test checks \"buy\" " +
                        "action with the second variant of coffee"
                    )
                ),

                (
                    test5_input,
                    (
                        -200,
                        -100,
                        -12,
                        -1,
                        6,
                        "This test checks \"buy\" " +
                        "action with the third variant of coffee"
                    )
                ),
                (
                    test6_input,
                    (
                        0,
                        0,
                        0,
                        0,
                        -550,
                        "This test checks \"take\" action"
                    )
                ),

                (
                    test7_input,
                    (
                        0,
                        0,
                        0,
                        0,
                        0,
                        "This test checks \"back\" " +
                        "action right after \"buy\" action"
                    )
                ),
            ]
        )

    def check(self, reply: str, clue: Any) -> CheckResult:
        if len(reply.splitlines()) <= 1:
            return CheckResult.wrong('Too few lines in output')

        water_, milk_, beans_, cups_, money_, feedback = clue

        milk = []
        water = []
        beans = []
        cups = []
        money = []

        for line in reply.splitlines():
            line = line.replace('$', '').strip()
            if len(line.split()) == 0:
                continue
            first_word = line.split()[0]
            if not first_word.isdigit():
                continue
            amount = int(first_word)
            if 'milk' in line:
                milk += amount,
            elif 'water' in line:
                water += amount,
            elif 'beans' in line:
                beans += amount,
            elif 'cups' in line:
                cups += amount,
            elif 'money' in line or 'cash' in line:
                money += amount,

        if len(milk) != 2:
            return CheckResult.wrong(
                "There should be two lines with \"milk\", " +
                f"found: {len(milk)}"
            )

        if len(water) != 2:
            return CheckResult.wrong(
                "There should be two lines with \"water\", " +
                f"found: {len(water)}"
            )

        if len(beans) != 2:
            return CheckResult.wrong(
                "There should be two lines with \"beans\", " +
                f"found: {len(beans)}"
            )

        if len(cups) != 2:
            return CheckResult.wrong(
                "There should be two lines with \"cups\", " +
                f"found: {len(cups)}"
            )

        if len(money) != 2:
            return CheckResult.wrong(
                "There should be two lines with \"money\", " +
                f"found: {len(money)}"
            )

        milk = milk[0], milk[-1]
        water = water[0], water[-1]
        beans = beans[0], beans[-1]
        cups = cups[0], cups[-1]
        money = money[0], money[-1]

        diff = lambda item: item[1] - item[0]

        is_correct = (
                diff(water) == water_ and
                diff(milk) == milk_ and
                diff(beans) == beans_ and
                diff(cups) == cups_ and
                diff(money) == money_
        )
        return CheckResult(is_correct, feedback)
