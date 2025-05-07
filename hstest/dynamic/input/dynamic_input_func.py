from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from hstest import CheckResult

    InputFunction = Callable[[str], str | CheckResult]
    DynamicTestFunction = Callable[[], str | None]


class DynamicInputFunction:
    def __init__(self, trigger_count: int, func: InputFunction) -> None:
        self.trigger_count = trigger_count
        self.input_function = func

    def trigger(self) -> None:
        if self.trigger_count > 0:
            self.trigger_count -= 1
