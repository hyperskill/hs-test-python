from hstest.stage_test import *
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest
from hstest.check_result import CheckResult

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)

OUTPUT = """
Starting to make a coffee
Grinding coffee beans
Boiling water
Mixing boiled water with crushed coffee beans
Pouring coffee into the cup
Pouring some milk into the cup
Coffee is ready!
"""


class CoffeeMachineTest(UserErrorTest):
    contain = [
        'Exception in test #1',
        r"""
        main.js:2
        console.log(`Starting to make a coffee
        """,
        'SyntaxError: missing ) after argument list'
    ]

    not_contain = 'Traceback'

    def generate(self) -> List[TestCase]:
        return TestCase.from_stepik([('', OUTPUT)])

    def check(self, reply: str, clue: Any) -> CheckResult:
        return CheckResult(
            reply.strip() == clue.strip(),
            'You should make coffee exactly like in the example')
