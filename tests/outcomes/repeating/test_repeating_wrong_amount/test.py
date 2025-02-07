from hstest.check_result import correct
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.testing.unittest.unexepected_error_test import UnexpectedErrorTest


class TestRepeatingWrongAmount(UnexpectedErrorTest):
    contain = 'UnexpectedError: Dynamic test "test" should not be repeated < 0 times, found -1'

    @dynamic_test(repeat=-1)
    def test(self, x):
        return correct()
