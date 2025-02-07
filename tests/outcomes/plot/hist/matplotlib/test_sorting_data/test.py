from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.hist.test_hist_drawing import test_hist_drawing


class TestMatplotlibHist(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = [
            [3, 2, 1],
            [3, 2, "1"],
            ["3", "2", "1"],
            [3.1, 2.1, 1],
            ["b", "a", "c"],
            [1, 5, 2, "1"],
        ]

        return test_hist_drawing(
            self.all_figures(), correct_data, DrawingLibrary.matplotlib
        )
