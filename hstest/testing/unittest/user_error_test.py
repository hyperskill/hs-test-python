from __future__ import annotations

from hstest.testing.unittest.expected_fail_test import ExpectedFailTest


class UserErrorTest(ExpectedFailTest):
    contain = ["No tests found"]
    _base_contain = []
    _base_not_contain = []
    not_contain = []
