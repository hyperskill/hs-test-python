from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestDynamicMethodEarlyExit(UserErrorTest):
    contain = """
    Error in test #1

    The program main.py has unexpectedly terminated.
    It finished execution too early, should continue running.
    
    Please find below the output of your program during this failed test.
    Note that the '>' character indicates the beginning of the input line.
    
    ---
    
    Server started!
    > main
    S1: main
    """  # noqa: W293

    @dynamic_test
    def test(self):
        pr = TestedProgram('main')

        out1 = pr.start()
        if out1 != "Server started!\n":
            return wrong("")

        out1 = pr.execute("main")
        if out1 != "S1: main\n":
            return wrong("")

        pr.execute("main2")
        return correct()
