from __future__ import annotations

from threading import current_thread, Lock
from typing import Any, TYPE_CHECKING

from hstest.dynamic.input.input_handler import InputHandler
from hstest.dynamic.output.output_handler import OutputHandler
from hstest.dynamic.security.exit_handler import ExitHandler
from hstest.dynamic.security.thread_handler import ThreadHandler
from hstest.exception.outcomes import ErrorWithFeedback

if TYPE_CHECKING:
    from hstest.dynamic.input.dynamic_input_func import DynamicTestFunction
    from hstest.dynamic.input.input_mock import Condition


class SystemHandler:
    __lock = Lock()
    __locked: bool = False
    __locker_thread = None

    @staticmethod
    def set_up() -> None:
        SystemHandler._lock_system_for_testing()

        OutputHandler.replace_stdout()
        InputHandler.replace_input()
        ExitHandler.replace_exit()
        ThreadHandler.install_thread_group()

    @staticmethod
    def tear_down() -> None:
        SystemHandler._unlock_system_for_testing()

        OutputHandler.revert_stdout()
        InputHandler.revert_input()
        ExitHandler.revert_exit()
        ThreadHandler.uninstall_thread_group()

    @staticmethod
    def _lock_system_for_testing() -> None:
        with SystemHandler.__lock:
            if SystemHandler.__locked:
                msg = "Cannot start the testing process more than once"
                raise ErrorWithFeedback(msg)
            SystemHandler.__locked = True
            SystemHandler.__locker_thread = current_thread()

    @staticmethod
    def _unlock_system_for_testing() -> None:
        if current_thread() != SystemHandler.__locker_thread:
            msg = "Cannot tear down the testing process from the other thread"
            raise ErrorWithFeedback(msg)

        with SystemHandler.__lock:
            if not SystemHandler.__locked:
                msg = "Cannot tear down the testing process more than once"
                raise ErrorWithFeedback(msg)
            SystemHandler.__locked = False
            SystemHandler.__locker_thread = None

    @staticmethod
    def install_handler(obj: Any, condition: Condition, input_func: DynamicTestFunction) -> None:
        InputHandler.install_input_handler(obj, condition, input_func)
        OutputHandler.install_output_handler(obj, condition)

    @staticmethod
    def uninstall_handler(obj: Any) -> None:
        InputHandler.uninstall_input_handler(obj)
        OutputHandler.uninstall_output_handler(obj)
