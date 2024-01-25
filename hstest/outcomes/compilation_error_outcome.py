from __future__ import annotations

from typing import TYPE_CHECKING

from hstest.outcomes.outcome import Outcome

if TYPE_CHECKING:
    from hstest.exception.outcomes import CompilationError


class CompilationErrorOutcome(Outcome):
    def __init__(self, ex: CompilationError) -> None:
        super().__init__()
        self.test_number = -1
        self.error_text = ex.error_text

    def get_type(self) -> str:
        return "Compilation error"
