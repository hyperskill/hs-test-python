from hstest.check_result import correct
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class InfiniteLoopTestLine1(UserErrorTest):
    contain = """
    Error in test #1

    Infinite loop detected.
    Last 100 lines your program printed are the same.
    """

    @dynamic_test
    def test(self):
        main = TestedProgram('main')
        main.start()
        return correct()
