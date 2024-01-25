from __future__ import annotations

from threading import current_thread, Thread


class ThreadGroup:
    def __init__(self, name: str | None = None) -> None:
        if name:
            self._name: str = name
        else:
            from hstest import StageTest

            test_num = StageTest.curr_test_global
            self._name = f"Test {test_num}"

        self.threads: list[Thread] = []

        curr = current_thread()
        if hasattr(curr, "_group"):
            self._parent: ThreadGroup | None = curr._group
        else:
            self._parent: ThreadGroup | None = None

    @property
    def name(self):
        return self._name

    @property
    def parent(self):
        return self._parent

    def add(self, thread: Thread) -> None:
        self.threads.append(thread)

    @staticmethod
    def curr_group() -> ThreadGroup:
        return getattr(current_thread(), "_group", None)
