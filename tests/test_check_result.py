import unittest
from hstest.check_result import CheckResult


class TestCheckResult(unittest.TestCase):
    def test_true(self):
        r = CheckResult.correct()
        self.assertTrue(r.result)
        self.assertEqual(r.feedback, '')

    def test_false(self):
        r = CheckResult.wrong('hello')
        self.assertFalse(r.result)
        self.assertEqual(r.feedback, 'hello')
