from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from hstest.common.utils import clean_text
from hstest.dynamic.output.infinite_loop_detector import loop_detector
from hstest.dynamic.output.output_handler import OutputHandler

if TYPE_CHECKING:
    from hstest.dynamic.input.dynamic_input_func import DynamicTestFunction


class DynamicInputHandler:
    def __init__(self, func: DynamicTestFunction):
        self._dynamic_input_function: DynamicTestFunction = func
        self._input_lines: List[str] = []

    def eject_next_line(self) -> Optional[str]:
        if len(self._input_lines) == 0:
            self._eject_next_input()
            if len(self._input_lines) == 0:
                return None

        next_line = self._input_lines.pop(0) + '\n'
        OutputHandler.inject_input('> ' + next_line)
        loop_detector.input_requested()
        return next_line

    def _eject_next_input(self):
        new_input = self._dynamic_input_function()

        if new_input is None:
            return

        new_input = clean_text(new_input)

        if new_input.endswith('\n'):
            new_input = new_input[:-1]

        self._input_lines += new_input.split('\n')
