from typing import Any

from hstest.check_result import CheckResult, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestDynamicMethodUnexpectedErrorNoCheckMethod(UserErrorTest):
    contain = """
    Wrong answer in test #1

    WA1
    """

    @dynamic_test
    def test(self):
        main = TestedProgram('main')
        main.start()
        main.execute('main')
        main.execute("main2")
        return None

    def check(self, reply: str, attach: Any) -> CheckResult:
        return wrong("WA1")
