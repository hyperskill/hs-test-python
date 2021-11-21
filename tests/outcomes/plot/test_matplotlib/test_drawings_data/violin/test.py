import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestMatplotlibViolin(PlottingTest):
    @dynamic_test
    def test(self):

        import matplotlib
        import pandas as pd
        import numpy as np

        program = TestedProgram()
        program.start()

        if len(self.all_figures) != 4:
            return wrong(f'Expected 4 plots to be plotted using matplotlib library, found {len(self.all_figures)}')

        correct_data = [[1, 2, 4], [2], [1], [1, 2, 5]]

        for i in range(len(self.all_figures)):
            violin = self.all_figures[i]
            if violin.type != 'violin':
                return wrong(f'Wrong drawing type {violin.type}. Expected violin')

            if 'x' not in violin.data:
                return wrong(f"Expected 'x' keys in the data dict of the violin drawing")

            if not isinstance(violin.data['x'], np.ndarray):
                return wrong("The 'x' value should be a ndarray")

            drawing_x_data = violin.data['x']

            if not np.array_equal(correct_data[i], drawing_x_data):
                return wrong('Wrong data of the violin graph')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestMatplotlibViolin('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
