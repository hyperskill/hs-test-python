import unittest

from hstest import CheckResult, TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.hist.test_hist_drawing import test_hist_drawing


class TestGroupBy(PlottingTest):

    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = [
            [14.55, 11.13, 16.17, 19.14, 13.72, 8.94, 21.87, 15.44],
            [15.2, 13.85, 11.55, 17.37, 12.9, 13.53, 18.22, 24.93, 17.93, 18.6],
        ]

        all_figs = self.all_figures()

        res1 = test_hist_drawing(all_figs[:2], correct_data, DrawingLibrary.pandas)
        res2 = test_hist_drawing(all_figs[2:], correct_data, DrawingLibrary.matplotlib)

        return CheckResult(res1.is_correct and res2.is_correct, res1.feedback + "\n" + res2.feedback)


class Test(unittest.TestCase):
    def test(self):
        status, feedback = TestGroupBy().run_tests()
        self.assertEqual(status, 0)


if __name__ == '__main__':
    Test().test()
