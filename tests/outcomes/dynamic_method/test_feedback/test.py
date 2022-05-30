from hstest.check_result import CheckResult
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestFeedback(UserErrorTest):
    contain = """
    Wrong answer in test #1

    feedback 2
    
    feedback 1
    """

    @dynamic_test(feedback="feedback 1")
    def test(self):
        return CheckResult.wrong("feedback 2")
