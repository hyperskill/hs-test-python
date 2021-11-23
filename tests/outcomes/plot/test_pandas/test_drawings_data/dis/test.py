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

        if len(self.all_figures) != 8:
            return wrong(f'Expected 8 plots to be plotted using pandas library, found {len(self.all_figures)}')

        correct_x = [
            [4, 4, 4.5, 5, 5.5, 6, 6],
            [1, 2, 2.5, 3, 3.5, 4, 5],
            [1, 2, 2.5, 3, 3.5, 4, 5],
            [4, 4, 4.5, 5, 5.5, 6, 6],
            [4, 4, 4.5, 5, 5.5, 6, 6],
            [1, 2, 2.5, 3, 3.5, 4, 5],
            [1, 2, 2.5, 3, 3.5, 4, 5],
            [4, 4, 4.5, 5, 5.5, 6, 6]
        ]

        for i, dis in enumerate(self.all_figures):
            if dis.type != 'dis':
                return wrong(f'Wrong drawing type {dis.type}. Expected dis')

            if 'x' not in dis.data:
                return wrong(f"Expected 'x' key in the data dict of the dis drawing")

            if not isinstance(dis.data['x'], np.ndarray):
                return wrong("The 'x' value should be a ndarray")

            drawing_x_data = dis.data['x']

            if not np.array_equal(correct_x[i], drawing_x_data):
                return wrong('Wrong data of the dis graph')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestPandasScatter('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
