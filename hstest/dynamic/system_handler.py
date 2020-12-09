from hstest.dynamic.input.input_handler import InputHandler
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.dynamic.security.exit_handler import ExitHandler


class SystemHandler:
    @staticmethod
    def set_up():
        OutputHandler.replace_stdout()
        InputHandler.replace_input()
        ExitHandler.replace_exit()

    @staticmethod
    def tear_down():
        OutputHandler.revert_stdout()
        InputHandler.revert_input()
        ExitHandler.revert_exit()
