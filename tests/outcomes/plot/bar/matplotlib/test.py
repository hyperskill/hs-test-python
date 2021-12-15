import unittest

import numpy as np

from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.bar.test_bar_drawing import test_bar_drawing


class TestMatplotlibBar(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = np.array([
            [(1, ''), (2, ''), (4, ''), (6, '')],
            [(1, ''), (2, ''), (4, ''), (6, '')],
            [(1, ''), (2, ''), (4, ''), (6, '')],
            [(1, ''), (2, ''), (4, ''), (6, '')],
        ], dtype=object)

        return test_bar_drawing(self.all_figures(), 4, correct_data, DrawingLibrary.matplotlib)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestMatplotlibBar('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
