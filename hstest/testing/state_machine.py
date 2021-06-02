from threading import Condition
from typing import Any, Callable, Dict, Set

from hstest.exception.outcomes import UnexpectedError


class StateMachine:
    def __init__(self, initial_value: Any):
        self._state: Any = initial_value
        self._transitions: Dict[Any, Set[Any]] = {}
        self.cv = Condition()

    def add_transition(self, fr: Any, to: Any):
        if fr not in self._transitions:
            self._transitions[fr] = set()
        self._transitions[fr].add(to)

    @property
    def state(self) -> Any:
        return self._state

    def in_state(self, state: Any):
        return self.state == state

    def set_and_wait(self, new_state: Any, waiting_state: Any = None):
        with self.cv:
            self.set_state(new_state)

            if waiting_state is None:
                self.wait_not_state(new_state)
            else:
                self.wait_state(waiting_state)

    def wait_state(self, waiting_state: Any):
        with self.cv:
            self._wait_while(lambda: self.state != waiting_state)

    def wait_not_state(self, state_to_avoid: Any):
        with self.cv:
            self._wait_while(lambda: self.state == state_to_avoid)

    def wait_not_states(self, *states_to_avoid: Any):
        def wait_func():
            for curr_state in states_to_avoid:
                if self.state == curr_state:
                    return True
            return False
        with self.cv:
            self._wait_while(wait_func)

    def _wait_while(self, check_wait: Callable[[], bool]):
        with self.cv:
            while check_wait():
                self.cv.wait()

    def set_state(self, new_state: Any):
        with self.cv:
            if new_state not in self._transitions[self.state]:
                raise UnexpectedError(
                    "Cannot transit from " + self.state + " to " + new_state)
            self._state = new_state
            self.cv.notify_all()
