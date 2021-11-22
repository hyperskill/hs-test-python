import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestPandasScatter(PlottingTest):
    @dynamic_test
    def test(self):

        import matplotlib
        import pandas as pd
        import numpy as np

        program = TestedProgram()
        program.start()

        if len(self.all_figures) != 3:
            return wrong(f'Expected 3 plots to be plotted using pandas library, found {len(self.all_figures)}')

        correct_x = [['Col1'], ['Col1'], ['Col2']]
        correct_y = [[1, 3], [1, 3], [2, 4]]

        for i, box in enumerate(self.all_figures):
            if box.type != 'box':
                return wrong(f'Wrong drawing type {box.type}. Expected box')

            if 'x' not in box.data or 'y' not in box.data:
                return wrong(f"Expected 'x', 'y' keys in the data dict of the box drawing")

            if not isinstance(box.data['x'], np.ndarray):
                return wrong("The 'x' value should be a ndarray")

            if not isinstance(box.data['y'], np.ndarray):
                return wrong("The 'y' value should be a ndarray")

            drawing_x_data = box.data['x']
            drawing_y_data = box.data['y']

            if not np.array_equal(correct_x[i], drawing_x_data) or not np.array_equal(correct_y[i], drawing_y_data):
                return wrong('Wrong data of the box graph')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestPandasScatter('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
