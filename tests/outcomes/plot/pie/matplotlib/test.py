import unittest

import numpy as np

from tests.outcomes.plot.pie.test_pie_drawing import test_pie_drawing
from hstest.testing.plotting.drawing import DrawingLibrary
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestMatplotlibPie(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = np.array([
            [['Mercury', 0.33], ['Venus', 4.87], ['Earth', 5.97]],
            [['', 2439.7], ['', 6051.8], ['', 6378.1]]
        ], dtype=object)

        return test_pie_drawing(self.all_figures, 2, correct_data, DrawingLibrary.matplotlib)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestMatplotlibPie('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
