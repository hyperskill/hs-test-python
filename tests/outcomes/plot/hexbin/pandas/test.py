import unittest

from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.hexbin.test_hexbin_drawing import test_hexbin_drawing


class TestPandasHexbin(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        return test_hexbin_drawing(self.all_figures(), 1, DrawingLibrary.pandas)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestPandasHexbin().run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
