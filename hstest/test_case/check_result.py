from typing import Optional

from hstest.exception.outcomes import TestPassed, WrongAnswer


class CheckResult:

    def __init__(self, result: bool, feedback: str):
        self._result: bool = result
        self._feedback: str = feedback

    @property
    def is_correct(self) -> bool:
        return self._result

    @property
    def feedback(self) -> str:
        return self._feedback

    @staticmethod
    def correct() -> 'CheckResult':
        return CheckResult(True, '')

    @staticmethod
    def wrong(feedback: str) -> 'CheckResult':
        return CheckResult(False, feedback)

    @staticmethod
    def from_error(error: BaseException) -> Optional['CheckResult']:
        if isinstance(error, TestPassed):
            return correct()
        elif isinstance(error, WrongAnswer):
            return wrong(error.feedback)
        else:
            return None


def correct() -> CheckResult:
    return CheckResult.correct()


def wrong(feedback: str) -> CheckResult:
    return CheckResult.wrong(feedback)
