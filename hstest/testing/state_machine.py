from __future__ import annotations

from threading import Condition
from typing import Any, TYPE_CHECKING

from hstest.exception.outcomes import UnexpectedError

if TYPE_CHECKING:
    from collections.abc import Callable


class StateMachine:
    def __init__(self, initial_value: Any) -> None:
        self._state: Any = initial_value
        self._transitions: dict[Any, set[Any]] = {}
        self.cv = Condition()

    def add_transition(self, fr: Any, to: Any) -> None:
        if fr not in self._transitions:
            self._transitions[fr] = set()
        self._transitions[fr].add(to)

    @property
    def state(self) -> Any:
        return self._state

    def in_state(self, state: Any) -> bool:
        return self.state == state

    def set_and_wait(self, new_state: Any, waiting_state: Any = None) -> None:
        with self.cv:
            self.set_state(new_state)

            if waiting_state is None:
                self.wait_not_state(new_state)
            else:
                self.wait_state(waiting_state)

    def wait_state(self, waiting_state: Any) -> None:
        with self.cv:
            self._wait_while(lambda: self.state != waiting_state)

    def wait_not_state(self, state_to_avoid: Any) -> None:
        with self.cv:
            self._wait_while(lambda: self.state == state_to_avoid)

    def wait_not_states(self, *states_to_avoid: Any) -> None:
        def wait_func() -> bool:
            return any(self.state == curr_state for curr_state in states_to_avoid)

        with self.cv:
            self._wait_while(wait_func)

    def _wait_while(self, check_wait: Callable[[], bool]) -> None:
        with self.cv:
            while check_wait():
                self.cv.wait()

    def set_state(self, new_state: Any) -> None:
        with self.cv:
            if new_state not in self._transitions[self.state]:
                raise UnexpectedError("Cannot transit from " + self.state + " to " + new_state)
            self._state = new_state
            self.cv.notify_all()
