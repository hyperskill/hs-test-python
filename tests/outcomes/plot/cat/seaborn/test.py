from hstest import TestedProgram
from hstest.dynamic.dynamic_test import dynamic_test
from hstest.stage import PlottingTest
from hstest.testing.plotting.drawing.drawing_library import DrawingLibrary
from tests.outcomes.plot.cat.test_cat_drawing import test_cat_drawing


class TestSeabornCat(PlottingTest):
    @dynamic_test
    def test(self):
        program = TestedProgram()
        program.start()

        return test_cat_drawing(self.all_figures(), 1, DrawingLibrary.seaborn)
