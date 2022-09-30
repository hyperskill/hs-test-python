from typing import Callable, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from hstest import CheckResult

    InputFunction = Callable[[str], Union[str, CheckResult]]
    DynamicTestFunction = Callable[[], Optional[str]]


class DynamicInputFunction:
    def __init__(self, trigger_count: int, func: InputFunction):
        self.trigger_count = trigger_count
        self.input_function = func

    def trigger(self):
        if self.trigger_count > 0:
            self.trigger_count -= 1
