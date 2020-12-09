import concurrent.futures.thread
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable


class DaemonThreadPoolExecutor(ThreadPoolExecutor):
    def __init__(self, max_workers: int = 1):
        super().__init__(max_workers=max_workers)

    def _remove_threads_from_queue(self):
        try:
            # Without this the Python interpreter cannot stop when the user writes an infinite loop
            # Even though all threads in ThreadPoolExecutor are created as daemon threads
            # They are not stopped on Python's shutdown but Python waits for them to stop on their own
            # See https://stackoverflow.com/a/49992422/13160001
            queue = concurrent.futures.thread._threads_queues
            for t in self._threads:
                if t in queue:
                    del queue[t]
        except BaseException:
            pass

    def submit(self, func: Callable, *args, **kwargs) -> Future:
        future: Future = super().submit(func, *args, **kwargs)
        self._remove_threads_from_queue()
        return future
