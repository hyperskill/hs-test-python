class Outcome:
    def __init__(self):
        self.test_number: int = 0
        self.error_text: str = ''
        self.stack_trace: str = ''

    def get_type(self) -> str:
        raise NotImplementedError()

    def get_type_suffix(self) -> str:
        return ''

    def __str__(self):
        if self.test_number == 0:
            when_error_happened = ' during testing'
        else:
            when_error_happened = f' in test #{self.test_number}'

        result = self.get_type() + when_error_happened + self.get_type_suffix()

        if self.error_text:
            result += '\n\n' + self.error_text.strip()

        if self.stack_trace:
            result += self.stack_trace.strip()

        # TODO add full log

        return result.strip()

    # TODO add get+outcome


class WrongAnswerOutcome(Outcome):
    def __init__(self, test_num: int, feedback: str):
        super().__init__()
        self.test_number = test_num
        self.error_text = feedback

    def get_type(self) -> str:
        return 'Wrong answer'


class ExceptionOutcome(Outcome):
    def __init__(self, test_num: int, cause: BaseException, feedback: str):
        super().__init__()
        self.test_number = test_num
        self.error_text = feedback
        # TODO add stack trace
        # TODO add no such element exception special feedback

    def get_type(self) -> str:
        return 'Exception'


class ErrorOutcome(Outcome):
    def __init__(self, test_num: int, cause: BaseException):
        super().__init__()
        self.test_number = test_num
        # TODO add time limit exception handle (maybe fs?)

    def get_type(self) -> str:
        return 'Error'


class FatalErrorOutcome(Outcome):
    def __init__(self, test_num: int, cause: BaseException):
        super().__init__()
        self.test_number = test_num
        # TODO add report, stacktrace

    def get_type(self) -> str:
        return 'Fatal error'

    def get_type_suffix(self) -> str:
        return ', please send the report to support@hyperskill.org'
