from typing import Any, List

from hstest import CheckResult, TestCase, StageTest


class TestImportRelativeError2(StageTest):
    source = 'main1'

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == 'main1\n', '')
