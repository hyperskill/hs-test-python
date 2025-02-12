from __future__ import annotations

from hstest.testing.unittest.expected_fail_test import ExpectedFailTest


class UnexpectedErrorTest(ExpectedFailTest):
    _base_contain = "Unexpected error"
    contain = ["Unexpected error during testing"]
