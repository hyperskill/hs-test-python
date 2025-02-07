from hstest.check_result import correct
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.dynamic.output.infinite_loop_detector import loop_detector
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class InfiniteLoopTestLine11(UserErrorTest):
    contain = """
    Error in test #1

    Infinite loop detected.
    No input request for the last 500 lines being printed.
    """

    @dynamic_test
    def test(self):
        main = TestedProgram("main")
        main.start()
        return correct()

    def test_run_unittest(self):
        before = loop_detector.check_no_input_requests_for_long
        loop_detector.check_no_input_requests_for_long = True

        super().test_run_unittest()

        loop_detector.check_no_input_requests_for_long = before
