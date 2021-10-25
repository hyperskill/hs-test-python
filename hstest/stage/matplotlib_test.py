from hstest.stage.stage_test import StageTest
from ..testing.plt_hack import hack


class MatplotlibTest(StageTest):
    def __init__(self, source: str = ''):
        super().__init__(source)
        self._drawings = []
        hack(self._drawings)

    @property
    def all_figures(self):
        return self._drawings
