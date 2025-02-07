import unittest
from typing import Any, List

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


@unittest.skip("takes too long")
class TestNoTimeLimit(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(time_limit=-1),
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult.correct()
