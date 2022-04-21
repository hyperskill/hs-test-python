from testing.unittest.expected_fail_test import ExpectedFailTest


class UnexpectedErrorTest(ExpectedFailTest):
    _base_contain = 'Unexpected error'
