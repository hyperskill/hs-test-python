import unittest

from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.hist.test_hist_drawing import test_hist_drawing


class TestPandasHist(PlottingTest):

    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = [
            [3, 2, 1],
            ['3', '2', '1'],
            [3.1, 2.1, 1],
            ['b', 'a', 'c']
        ]

        return test_hist_drawing(self.all_figures(), correct_data, DrawingLibrary.pandas)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestPandasHist(source_name='main').run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
