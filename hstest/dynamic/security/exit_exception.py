class ExitException(BaseException):
    @staticmethod
    def throw():
        raise ExitException()
