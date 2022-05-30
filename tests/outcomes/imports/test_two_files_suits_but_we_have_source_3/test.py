from typing import Any, List

from hstest import CheckResult, StageTest, TestCase


class TestImportRelativeError2(StageTest):
    source = 'main2'

    def generate(self) -> List[TestCase]:
        return [TestCase()]

    def check(self, reply: str, attach: Any) -> CheckResult:
        return CheckResult(reply == 'main2\n', '')
