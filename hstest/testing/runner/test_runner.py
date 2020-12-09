from typing import Optional

from hstest.check_result import CheckResult


class TestRunner:
    def test(self, test_run: 'TestRun') -> Optional[CheckResult]:
        raise NotImplementedError("Test method is not implemented")
