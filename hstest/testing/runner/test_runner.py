from __future__ import annotations

import typing

from hstest.check_result import CheckResult, correct

if typing.TYPE_CHECKING:
    from hstest.test_case.test_case import TestCase
    from hstest.testing.test_run import TestRun


class TestRunner:
    def set_up(self, test_case: TestCase) -> None:
        pass

    def tear_down(self, test_case: TestCase) -> None:
        pass

    def test(self, test_run: TestRun) -> CheckResult | None:
        return correct()
