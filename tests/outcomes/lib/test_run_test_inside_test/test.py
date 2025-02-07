from hstest.check_result import CheckResult
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.exception.outcomes import ErrorWithFeedback
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestRunTestInsideTest(UserErrorTest):
    contain = """
    Error in test #1

    Error during testing
    
    Cannot start the testing process more than once
    """  # noqa: W293

    @dynamic_test
    def test(self):
        status, feedback = TestRunTestInsideTest("").run_tests()
        if status != 0:
            raise ErrorWithFeedback(feedback)
        return CheckResult.correct()
