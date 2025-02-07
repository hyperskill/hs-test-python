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

        # should take into account "weights" column as well, not use weight=1
        correct_data = [[1, 2, 3, 4, 5]]

        return test_hist_drawing(
            self.all_figures(), correct_data, DrawingLibrary.matplotlib
        )
