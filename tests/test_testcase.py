from __future__ import annotations

import unittest

from hstest.exception.outcomes import UnexpectedError
from hstest.test_case import TestCase


class TestTestCase(unittest.TestCase):
    def test_attach_none_default(self) -> None:
        test_case = TestCase()
        self.assertIsNone(test_case.attach)

    def test_attach(self) -> None:
        attach = (1, "abc")
        test_case = TestCase(attach=attach)
        self.assertEqual(attach, test_case.attach)

    def test_copy_to_attach(self) -> None:
        test_case = TestCase(stdin="abc", copy_to_attach=True)
        self.assertEqual(test_case.attach, "abc")

    def test_copy_to_attach_exception(self) -> None:
        with self.assertRaises(UnexpectedError):
            TestCase(stdin="abc", attach=(1, 2, 3), copy_to_attach=True)

    def test_stdin_empty(self) -> None:
        test_case = TestCase()
        self.assertEqual(test_case.input, "")

    def test_stdin_passed(self) -> None:
        stdin = "abc"
        test_case = TestCase(stdin=stdin)
        self.assertEqual(test_case.input, stdin)

    def test_from_stepik_length(self) -> None:
        tests = TestCase.from_stepik(["123", "234", "345"])
        self.assertEqual(len(tests), 3)

    def test_from_stepik_simple(self) -> None:
        tests = TestCase.from_stepik(["123", "234", "345"])
        self.assertEqual(tests[0].input, "123")
        self.assertEqual(tests[0].attach, None)
        self.assertEqual(tests[1].input, "234")
        self.assertEqual(tests[1].attach, None)
        self.assertEqual(tests[2].input, "345")
        self.assertEqual(tests[2].attach, None)

    def test_from_stepik_with_attach(self) -> None:
        tests = TestCase.from_stepik([("123", 234), ("234", 345), ("345", 456)])
        self.assertEqual(tests[0].input, "123")
        self.assertEqual(tests[0].attach, 234)
        self.assertEqual(tests[1].input, "234")
        self.assertEqual(tests[1].attach, 345)
        self.assertEqual(tests[2].input, "345")
        self.assertEqual(tests[2].attach, 456)

    def test_from_stepik_mixed(self) -> None:
        tests = TestCase.from_stepik(
            [("mixed1", 234567), "mixed234", ("mixed345", 456234), "567"]
        )
        self.assertEqual(tests[0].input, "mixed1")
        self.assertEqual(tests[0].attach, 234567)
        self.assertEqual(tests[1].input, "mixed234")
        self.assertEqual(tests[1].attach, None)
        self.assertEqual(tests[2].input, "mixed345")
        self.assertEqual(tests[2].attach, 456234)
        self.assertEqual(tests[3].input, "567")
        self.assertEqual(tests[3].attach, None)

    def test_from_stepik_bad_data(self) -> None:
        with self.assertRaises(UnexpectedError):
            TestCase.from_stepik(
                [("mixed1", 234567), 234345, ("mixed345", 456234), "567"]
            )
