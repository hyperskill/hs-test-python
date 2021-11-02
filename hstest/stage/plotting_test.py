from hstest.stage.stage_test import StageTest
from hstest.testing.runner.plot_testing_runner import PlottingTestingRunner


class PlottingTest(StageTest):

    def __init__(self, source: str = ''):
        super().__init__(source)
        self._drawings = []
        self.runner = PlottingTestingRunner(self._drawings)

    @property
    def all_figures(self):
        return self._drawings
