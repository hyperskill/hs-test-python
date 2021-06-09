from hstest.exception.outcomes import CompilationError
from hstest.outcomes.outcome import Outcome


class CompilationErrorOutcome(Outcome):
    def __init__(self, ex: CompilationError):
        super().__init__()
        self.test_number = -1
        self.error_text = ex.error_text

    def get_type(self) -> str:
        return 'Compilation error'
