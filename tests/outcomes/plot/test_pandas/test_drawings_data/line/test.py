import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestPandasLine(PlottingTest):
    @dynamic_test
    def test(self):

        import matplotlib
        import pandas as pd
        import numpy as np

        program = TestedProgram()
        program.start()

        if len(self.all_figures) != 4:
            return wrong(f'Expected 4 plots to be plotted using pandas library, found {len(self.all_figures)}')

        correct_x = [0, 1, 2]
        correct_y = [1, 3, 2]

        for i in range(len(self.all_figures)):

            line = self.all_figures[i]

            correct_x = [2, 4, 6] if i > 1 else correct_x

            if line.type != 'line':
                return wrong(f'Wrong drawing type {line.type}. Expected line')

            if 'x' not in line.data or 'y' not in line.data:
                return wrong(f"Expected 'x', 'y' keys in the data dict of the line drawing")

            if not isinstance(line.data['x'], np.ndarray):
                return wrong("The 'x' value should be a ndarray")

            if not isinstance(line.data['y'], np.ndarray):
                return wrong("The 'y' value should be a ndarray")

            drawing_x_data = line.data['x']
            drawing_y_data = line.data['y']

            if not np.array_equal(correct_x, drawing_x_data) or not np.array_equal(correct_y, drawing_y_data):
                return wrong('Wrong data of the line graph')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestPandasLine('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
