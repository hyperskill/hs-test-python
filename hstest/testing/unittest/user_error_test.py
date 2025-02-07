from __future__ import annotations

from hstest.testing.unittest.expected_fail_test import ExpectedFailTest


class UserErrorTest(ExpectedFailTest):
    _base_not_contain = "Unexpected error"
