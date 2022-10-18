import unittest
from time import sleep

from hstest.check_result import wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.tested_program import TestedProgram
from hstest.testing.unittest.user_error_test import UserErrorTest


@unittest.skip('Background execution in python doesn\'t work')
class TestDynamicMethodStartInBackgroundWrongAnswer(UserErrorTest):
    contain = """
    Wrong answer in test #1

    Please find below the output of your program during this failed test.
    

    ---
    
    Server started!
    S1
    """  # noqa: W293

    @dynamic_test
    def test(self):
        server = TestedProgram('main')

        server.start_in_background()
        sleep(0.15)
        return wrong('')
