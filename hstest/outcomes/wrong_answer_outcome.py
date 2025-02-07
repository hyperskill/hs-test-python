from __future__ import annotations

from typing import TYPE_CHECKING

from hstest.outcomes.outcome import Outcome

if TYPE_CHECKING:
    from hstest.exception.outcomes import WrongAnswer


class WrongAnswerOutcome(Outcome):
    def __init__(self, test_num: int, ex: WrongAnswer) -> None:
        super().__init__(test_num, ex.feedback, "")

    def get_type(self) -> str:
        return "Wrong answer"
