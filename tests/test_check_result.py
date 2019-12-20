import unittest
from hstest.check_result import CheckResult, accept, wrong


class TestCheckResult(unittest.TestCase):
    def test_true(self):
        r = CheckResult.true()
        self.assertTrue(r.result)
        self.assertEqual(r.feedback, '')

    def test_false(self):
        r = CheckResult.false('hello')
        self.assertFalse(r.result)
        self.assertEqual(r.feedback, 'hello')

    def test_accept(self):
        r = accept()
        self.assertTrue(r.result)
        self.assertEqual(r.feedback, '')

    def test_wrong(self):
        r = wrong('fff')
        self.assertFalse(r.result)
        self.assertEqual(r.feedback, 'fff')
