from hstest.exception.outcomes import WrongAnswer
from hstest.outcomes.outcome import Outcome


class WrongAnswerOutcome(Outcome):
    def __init__(self, test_num: int, ex: WrongAnswer):
        super().__init__(test_num, ex.feedback, '')

    def get_type(self) -> str:
        return 'Wrong answer'
