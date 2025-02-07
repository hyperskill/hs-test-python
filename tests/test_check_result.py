from __future__ import annotations

import unittest

from hstest.check_result import CheckResult


class TestCheckResult(unittest.TestCase):
    def test_true(self) -> None:
        r = CheckResult.correct()
        self.assertTrue(r.is_correct)
        self.assertEqual(r.feedback, "")

    def test_false(self) -> None:
        r = CheckResult.wrong("hello")
        self.assertFalse(r.is_correct)
        self.assertEqual(r.feedback, "hello")
