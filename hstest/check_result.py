class CheckResult:

    def __init__(self, result: bool, feedback: str):
        self.result = result
        self.feedback = feedback

    @staticmethod
    def true():
        return CheckResult(True, '')

    @staticmethod
    def false(feedback: str = ''):
        return CheckResult(False, feedback)


def wrong(feedback: str = '') -> CheckResult:
    return CheckResult.false(feedback)


def accept():
    return CheckResult.true()
