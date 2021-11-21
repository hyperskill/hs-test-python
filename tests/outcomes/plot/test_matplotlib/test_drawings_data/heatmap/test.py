import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestMatplotlibHeatmap(PlottingTest):
    @dynamic_test
    def test(self):

        import matplotlib
        import pandas as pd
        import numpy as np

        program = TestedProgram()
        program.start()

        if len(self.all_figures) != 2:
            return wrong(f'Expected 2 plots to be plotted using matplotlib library, found {len(self.all_figures)}')

        correct_data = [
            [1, 2, 3],
            [7, 8, 9]
        ]

        for i in range(len(self.all_figures)):
            heatmap = self.all_figures[i]

            if heatmap.type != 'heatmap':
                return wrong(f'Wrong drawing type {heatmap.type}. Expected heatmap')

            if 'x' not in heatmap.data:
                return wrong(f"Expected 'x' keys in the data dict of the heatmap drawing")

            if not isinstance(heatmap.data['x'], np.ndarray):
                return wrong("The 'x' value should be a ndarray")

            drawing_x_data = heatmap.data['x']

            if not np.array_equal(correct_data, drawing_x_data):
                return wrong('Wrong data of the heatmap graph')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestMatplotlibHeatmap('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
