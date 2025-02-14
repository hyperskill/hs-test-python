from __future__ import annotations

from typing import TYPE_CHECKING

from hstest.stage.stage_test import StageTest
from hstest.testing.runner.plot_testing_runner import PlottingTestingRunner

if TYPE_CHECKING:
    from hstest.testing.plotting.drawing.drawing import Drawing


class PlottingTest(StageTest):
    def __init__(self, args="", *, source: str = "") -> None:
        super().__init__(args, source=source)
        self._all_drawings: list[Drawing] = []
        self._new_drawings: list[Drawing] = []
        self.runner = PlottingTestingRunner(self._all_drawings, self._new_drawings)

    def all_figures(self) -> list[Drawing]:
        return self._all_drawings

    def new_figures(self) -> list[Drawing]:
        result = self._new_drawings[:]
        self._new_drawings.clear()
        return result
