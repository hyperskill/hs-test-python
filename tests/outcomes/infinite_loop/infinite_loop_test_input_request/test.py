from time import sleep

from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class InfiniteLoopTestInputRequest(UserErrorTest):
    contain = """
    Error in test #1

    Program ran out of input. You tried to read more than expected.
    
    Please find below the output of your program during this failed test.
    
    ---
    
    Long Line Long Line Long Line
    """  # noqa: W293

    @dynamic_test
    def test(self):
        main = TestedProgram('main')
        main.start()
        main.stop_input()
        sleep(0.005)
        return None
