from threading import Thread, current_thread
from typing import List, Optional


class ThreadGroup:
    def __init__(self, name: str):
        self._name: str = name
        self.threads: List[Thread] = []

        curr = current_thread()
        if hasattr(curr, "_group"):
            self._parent: Optional[ThreadGroup] = curr._group
        else:
            self._parent: Optional[ThreadGroup] = None

    @property
    def name(self):
        return self._name

    @property
    def parent(self):
        return self._parent

    def add(self, thread: Thread):
        self.threads.append(thread)
