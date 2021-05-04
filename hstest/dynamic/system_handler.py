from threading import Lock, current_thread

from hstest.dynamic.input.input_handler import InputHandler
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.dynamic.security.exit_handler import ExitHandler
from hstest.exception.outcomes import ErrorWithFeedback


class SystemHandler:
    __lock = Lock()
    __locked: bool = False
    __locker_thread = None

    @staticmethod
    def set_up():
        with SystemHandler.__lock:
            if SystemHandler.__locked:
                raise ErrorWithFeedback(
                    "Cannot start the testing process more than once")
            SystemHandler.__locked = True
            SystemHandler.__locker_thread = current_thread()

        OutputHandler.replace_stdout()
        InputHandler.replace_input()
        ExitHandler.replace_exit()

    @staticmethod
    def tear_down():
        if current_thread() != SystemHandler.__locker_thread:
            raise ErrorWithFeedback(
                "Cannot tear down the testing process from the other thread")

        with SystemHandler.__lock:
            if not SystemHandler.__locked:
                raise ErrorWithFeedback(
                    "Cannot tear down the testing process more than once")
            SystemHandler.__locked = False
            SystemHandler.__locker_thread = None

        OutputHandler.revert_stdout()
        InputHandler.revert_input()
        ExitHandler.revert_exit()
