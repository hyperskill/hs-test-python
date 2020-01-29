from hstest.dynamic.handle_stdout import StdoutHandler
from hstest.dynamic.handle_stdin import StdinHandler
from hstest.dynamic.handle_exit import ExitHandler


class SystemHandler:
    @staticmethod
    def set_up():
        StdoutHandler.replace_stdout()
        StdinHandler.replace_stdin()
        ExitHandler.replace_exit()

    @staticmethod
    def tear_down():
        StdoutHandler.revert_stdout()
        StdinHandler.revert_stdin()
        ExitHandler.revert_exit()
