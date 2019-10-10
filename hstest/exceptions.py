
class BadSolutionException(Exception):
    def __init__(self, message):
        self.message = message


class SyntaxException(BadSolutionException):
    def __init__(self, message):
        super().__init__(message)


class ExitException(BadSolutionException):
    def __init__(self, message):
        super().__init__(message)
