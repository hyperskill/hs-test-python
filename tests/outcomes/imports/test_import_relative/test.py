import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


@unittest.skip('Relative imports doesn\'t work')
class TestImportRelative(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == '1035\n', '')
