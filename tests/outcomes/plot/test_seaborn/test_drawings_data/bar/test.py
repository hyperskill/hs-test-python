import unittest

from hstest.check_result import correct, wrong
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest import TestedProgram


class TestSeaborn(PlottingTest):
    @dynamic_test
    def test(self):

        import matplotlib
        import pandas as pd
        import numpy as np

        program = TestedProgram()
        program.start()

        if len(self.all_figures) != 2:
            return wrong(f'Expected 2 plots to be plotted using pandas library, found {len(self.all_figures)}')

        correct_data = np.array([1, 2, 3, 4, 5])

        for hist in (self.all_figures[0], self.all_figures[1]):
            if hist.type != 'hist':
                return wrong(f'Wrong drawing type {hist.type}. Expected hist')

            if 'x' not in hist.data:
                return wrong(f"Expected 'x' key in the data dict of the hist drawing")

            if not isinstance(hist.data['x'], np.ndarray):
                return wrong("The 'x' value should be a ndarray")

            drawing_data = hist.data['x']

            if not np.array_equal(correct_data, drawing_data):
                return wrong('Wrong data of the hist graph')

        return correct()


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestSeaborn('main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
