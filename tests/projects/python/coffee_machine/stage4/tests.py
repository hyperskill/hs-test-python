from hstest.stage_test import *
from hstest.test_case import TestCase
from hstest.check_result import CheckResult

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class CoffeeMachineTest(StageTest):
    def generate(self) -> List[TestCase]:
        return TestCase.from_stepik(
            [
                ('take\n',) * 2,
                ('buy\n1\n',) * 2,
                ('buy\n2\n',) * 2,
                ('buy\n3\n',) * 2,
                ('fill\n2001\n510\n101\n21\n',) * 2,
            ]
        )

    def check(self, reply: str, clue: Any) -> CheckResult:
        if len(reply.splitlines()) <= 1:
            return CheckResult.wrong('Too few output lines')

        action, *rest = clue.split()

        milk = []
        water = []
        beans = []
        cups = []
        money = []

        for line in reply.splitlines():
            if len(line.split()) == 0:
                continue
            first_word = line.split()[0]
            first_word = first_word.replace('$', '')
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
            elif 'money' in line:
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

        if water[0] != 400 or milk[0] != 540 or beans[0] != 120 or cups[0] != 9 or money[0] != 550:
            return CheckResult.wrong(
                "Initial setup is wrong: " +
                "coffee machine should be filled like " +
                "stated in the description"
            )

        diff = lambda item: item[1] - item[0]

        if action == 'take':
            if diff(milk) != 0:
                return CheckResult.wrong(
                    "After \"take\" action milk " +
                    "amount shouldn't be changed"
                )

            if diff(water) != 0:
                return CheckResult.wrong(
                    "After \"take\" action water " +
                    "amount shouldn't be changed"
                )

            if diff(beans) != 0:
                return CheckResult.wrong(
                    "After \"take\" action beans " +
                    "amount shouldn't be changed"
                )

            if diff(cups) != 0:
                return CheckResult.wrong(
                    "After \"take\" action cups " +
                    "amount shouldn't be changed"
                )

            if money[1] != 0:
                return CheckResult.wrong(
                    "After \"take\" action money " +
                    "amount should be zero"
                )

            return CheckResult.correct()

        elif action == 'buy':
            option = rest[0]
            if option == '1':

                if diff(water) != -250:
                    return CheckResult.wrong(
                        "After buying the first option " +
                        "water amount should be lowered by 250"
                    )

                if diff(milk) != 0:
                    return CheckResult.wrong(
                        "After buying the first option " +
                        "milk amount should not be changed"
                    )

                if diff(beans) != -16:
                    return CheckResult.wrong(
                        "After buying the first option " +
                        "beans amount should be lowered by 16"
                    )

                if diff(cups) != -1:
                    return CheckResult.wrong(
                        "After buying the first option " +
                        "cups amount should be lowered by 1"
                    )

                if diff(money) != 4:
                    return CheckResult.wrong(
                        "After buying the first option " +
                        "money amount should be increased by 4"
                    )

                return CheckResult.correct()

            elif option == '2':

                if diff(water) != -350:
                    return CheckResult.wrong(
                        "After buying the second option " +
                        "water amount should be lowered by 350"
                    )

                if diff(milk) != -75:
                    return CheckResult.wrong(
                        "After buying the second option " +
                        "milk amount should be lowered by 75"
                    )

                if diff(beans) != -20:
                    return CheckResult.wrong(
                        "After buying the second option " +
                        "beans amount should be lowered by 20"
                    )

                if diff(cups) != -1:
                    return CheckResult.wrong(
                        "After buying the second option " +
                        "cups amount should be lowered by 1"
                    )

                if diff(money) != 7:
                    return CheckResult.wrong(
                        "After buying the second option " +
                        "money amount should be increased by 7"
                    )

                return CheckResult.correct()

            elif option == '3':

                if diff(water) != -200:
                    return CheckResult.wrong(
                        "After buying the third option " +
                        "water amount should be lowered by 200"
                    )

                if diff(milk) != -100:
                    return CheckResult.wrong(
                        "After buying the third option " +
                        "milk amount should be lowered by 100"
                    )

                if diff(beans) != -12:
                    return CheckResult.wrong(
                        "After buying the third option " +
                        "beans amount should be lowered by 12"
                    )

                if diff(cups) != -1:
                    return CheckResult.wrong(
                        "After buying the third option " +
                        "cups amount should be lowered by 1"
                    )

                if diff(money) != 6:
                    return CheckResult.wrong(
                        "After buying the third option " +
                        "money amount should be increased by 6"
                    )

                return CheckResult.correct()

        elif action == 'fill':
            water_, milk_, beans_, cups_ = map(int, rest)

            if diff(money) != 0:
                return CheckResult.wrong(
                    "After \"fill\" action " +
                    "money amount should not be changed"
                )

            if diff(water) != water_:
                return CheckResult.wrong(
                    "After \"fill\" action " +
                    f"water amount expected to be increased by {water_}" +
                    f" but was increased by {diff(water)}"
                )

            if diff(milk) != milk_:
                return CheckResult.wrong(
                    "After \"fill\" action " +
                    f"milk amount expected to be increased by {milk_}" +
                    f" but was increased by {diff(milk)}"
                )

            if diff(beans) != beans_:
                return CheckResult.wrong(
                    "After \"fill\" action " +
                    f"beans amount expected to be increased by {beans_}" +
                    f" but was increased by {diff(beans)}"
                )

            if diff(cups) != cups_:
                return CheckResult.wrong(
                    "After \"fill\" action " +
                    f"cups amount expected to be increased by {cups_}" +
                    f" but was increased by {diff(cups)}"
                )

            return CheckResult.correct()

        return CheckResult.correct()
