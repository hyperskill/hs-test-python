import unittest

from tests.outcomes.plot.box.test_box_drawing import test_box_drawing
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestPandasBox(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        return test_box_drawing(self.all_figures, 2, DrawingLibrary.pandas)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestPandasBox('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
