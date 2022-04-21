from typing import Any, List

from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.testing.unittest.user_error_test import UserErrorTest


class ExceptionWhileReading(UserErrorTest):
    contain = [
        'Exception in test #2',
        'Traceback (most recent call last):',
        '    print(get_line())',
        '    return get_num()',
        '    return get()',
        '    return int(input())',
        'ValueError: invalid literal for int() with base 10: \'strange\''
    ]

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin='1'),
            TestCase(stdin='strange')
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(True, '')
