from typing import List

from hstest.stage.stage_test import StageTest
from hstest.testing.plotting.drawing.drawing import Drawing
from hstest.testing.runner.plot_testing_runner import PlottingTestingRunner


class PlottingTest(StageTest):

    def __init__(self, source: str = ''):
        super().__init__(source)
        self._all_drawings: List[Drawing] = []
        self._new_drawings: List[Drawing] = []
        self.runner = PlottingTestingRunner(self._all_drawings, self._new_drawings)

    @property
    def all_figures(self) -> List[Drawing]:
        return self._all_drawings

    def new_figures(self) -> List[Drawing]:
        result = self._new_drawings[:]
        self._new_drawings.clear()
        return result
