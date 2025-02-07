import numpy as np

from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.bar.test_bar_drawing import test_bar_drawing


class TestSeabornBar(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = np.array(
            [
                [["A", 10], ["B", 30], ["C", 20]],
                [["", 10], ["", 30], ["", 20]],
                [[10, ""], [30, ""], [20, ""]],
            ],
            dtype=object,
        )

        return test_bar_drawing(
            self.all_figures(), correct_data, DrawingLibrary.seaborn
        )
