class CheckResult:

    def __init__(self, result: bool, feedback: str):
        self.result = result
        self.feedback = feedback

    @staticmethod
    def correct():
        return CheckResult(True, '')

    @staticmethod
    def wrong(feedback) -> 'CheckResult':
        return CheckResult(False, feedback)
