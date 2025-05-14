from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


class TestDynamicMethodException(UserErrorTest):
    contain = [
        """
        Exception in test #1

        Traceback (most recent call last):
          File "main.py", line 3, in <module>
            print(0/0)
                  ~^~
        ZeroDivisionError: division by zero
        
        Please find below the output of your program during this failed test.
        Note that the '>' character indicates the beginning of the input line.
        
        ---
        
        Server started!
        > main
        S1: main
        """
    ]

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
