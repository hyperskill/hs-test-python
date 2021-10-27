from threading import current_thread, Thread
from typing import Callable, Optional

from hstest.dynamic.security.thread_group import ThreadGroup


class ThreadHandler:

    _group = None
    _old_init: Optional[Callable[[], Thread]] = None

    @classmethod
    def install_thread_group(cls):
        if cls._old_init is None:
            cls._old_init = Thread.__init__
            Thread.__init__ = ThreadHandler.init
            cls._group = ThreadGroup('Main')
            current_thread()._group = cls._group

    @classmethod
    def uninstall_thread_group(cls):
        if cls._old_init is not None:
            Thread.__init__ = cls._old_init
            cls._old_init = None
            del current_thread()._group
            cls._group = None

    @staticmethod
    def init(self, group=None, target=None, name=None,
             args=(), kwargs=None, *, daemon=None):

        ThreadHandler._old_init(self, None, target, name, args, kwargs, daemon=daemon)

        # Custom addition to Thread class (implement thread groups)
        if group is not None:
            self._group = group
        else:
            curr = current_thread()

            if hasattr(curr, '_group'):
                self._group = curr._group
            else:
                self._group = ThreadGroup(self._name)

        self._group.add(self)
