from hstest import dynamic_test, PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from hstest.testing.tested_program import TestedProgram
from tests.outcomes.plot.bar.test_bar_drawing import test_bar_drawing


class Cleaning(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = [
            [[1, 2], [2, 2], [3, 2], [5, 1], [6, 4], [7, 1], [8, 1]],
            [[1, 1], [2, 1], [3, 3], [4, 2], [6, 1], [7, 1], [8, 2]],
        ]

        return test_bar_drawing(self.all_figures(), correct_data, DrawingLibrary.pandas)
