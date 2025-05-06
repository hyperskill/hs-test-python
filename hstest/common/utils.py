from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

failed_msg_start = "#educational_plugin FAILED + "
failed_msg_continue = "#educational_plugin "
success_msg = "#educational_plugin test OK"


def failed(message: str, *, is_unittest: bool) -> tuple[int, str]:
    """Reports failure.

    Args:
        message: Message to print
        is_unittest: Flag indicating if the function is called from unittest

    Returns:
        tuple: A tuple containing (-1, message)
    """
    if not is_unittest:
        lines = message.splitlines()
        print("\n" + failed_msg_start + lines[0])  # noqa: T201
        for line in lines[1:]:
            print(failed_msg_continue + line)  # noqa: T201
    return -1, message


def passed(*, is_unittest: bool) -> tuple[int, str]:
    """Reports success.

    Returns:
        tuple: A tuple containing (0, "test OK")
    """
    if not is_unittest:
        print("\n" + success_msg)  # noqa: T201
    return 0, "test OK"


def clean_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").replace("\u00a0", "\u0020")


def try_many_times(times_to_try: int, sleep_time_ms: int, exit_func: Callable[[], bool]) -> bool:
    while times_to_try > 0:
        times_to_try -= 1
        if exit_func():
            return True
        sleep(sleep_time_ms / 1000)
    return False
