# deprecated, but old tests use "from hstest.check_result import CheckResult"
# new way to import is "from hstest import CheckResult"
from __future__ import annotations

from hstest.test_case import CheckResult, correct, wrong  # noqa: F401
