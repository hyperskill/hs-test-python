import numpy as np

from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.pie.test_pie_drawing import test_pie_drawing


class TestMatplotlibPie(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        correct_data = np.array([
            [['Mercury', 0.33], ['Venus', 4.87], ['Earth', 5.97]],
            [['', 2439.], ['', 6051.8], ['', 6378.1]]
        ], dtype=object)

        return test_pie_drawing(self.all_figures(), 1, correct_data, DrawingLibrary.matplotlib)
