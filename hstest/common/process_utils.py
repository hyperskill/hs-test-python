from __future__ import annotations

import threading
import weakref
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures.thread import _worker
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hstest.dynamic.security.thread_group import ThreadGroup


class DaemonThreadPoolExecutor(ThreadPoolExecutor):
    def __init__(
        self, max_workers: int = 1, name: str = "", group: ThreadGroup = None
    ) -> None:
        super().__init__(max_workers=max_workers, thread_name_prefix=name)
        self.group = group

    # Adjusted method from the ThreadPoolExecutor class just to create threads as daemons
    def _adjust_thread_count(self) -> None:
        if self._idle_semaphore.acquire(timeout=0):
            return

        # When the executor gets lost, the weakref callback will wake up
        # the worker threads.
        def weakref_cb(_, q=self._work_queue) -> None:
            q.put(None)

        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            thread_name = "%s_%d" % (self._thread_name_prefix or self, num_threads)

            args = (
                weakref.ref(self, weakref_cb),
                self._work_queue,
                self._initializer,
                self._initargs,
            )

            t = threading.Thread(
                name=thread_name, target=_worker, args=args, group=self.group
            )
            t.daemon = True
            t.start()
            self._threads.add(t)


def is_port_in_use(port):
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0
