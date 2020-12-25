from typing import Optional

from hstest.check_result import CheckResult


class TestRunner:
    def set_up(self, test_case: 'TestCase'):
        pass

    def tear_down(self, test_case: 'TestCase'):
        pass

    def test(self, test_run: 'TestRun') -> Optional[CheckResult]:
        raise NotImplementedError("Test method is not implemented")
