import sys
from threading import _newname, current_thread, Event, _dangling, Thread
from typing import Callable, Optional

from hstest.dynamic.security.thread_group import ThreadGroup


class ThreadHandler:

    _old_init: Optional[Callable[[], Thread]] = None

    @classmethod
    def install_thread_group(cls):
        if cls._old_init is None:
            cls._old_init = Thread.__init__
            Thread.__init__ = ThreadHandler.init

    @classmethod
    def uninstall_thread_group(cls):
        if cls._old_init is not None:
            Thread.__init__ = cls._old_init
            cls._old_init = None

    @staticmethod
    def init(self, group=None, target=None, name=None,
             args=(), kwargs=None, *, daemon=None):

        assert group is None or isinstance(group, ThreadGroup), "group argument must be None for now"

        if kwargs is None:
            kwargs = {}

        self._target = target

        if sys.version_info >= (3, 10):
            if name:
                name = str(name)
            else:
                name = _newname("Thread-%d")
                if target is not None:
                    try:
                        target_name = target.__name__
                        name += f" ({target_name})"
                    except AttributeError:
                        pass
            self._name = name

        else:
            self._name = str(name or _newname())

        self._args = args
        self._kwargs = kwargs
        if daemon is not None:
            self._daemonic = daemon
        else:
            self._daemonic = current_thread().daemon
        self._ident = None

        if sys.version_info >= (3, 8):
            from threading import _HAVE_THREAD_NATIVE_ID
            if _HAVE_THREAD_NATIVE_ID:
                self._native_id = None

        self._tstate_lock = None
        self._started = Event()
        self._is_stopped = False
        self._initialized = True

        self._stderr = sys.stderr

        if sys.version_info >= (3, 8):
            from threading import _make_invoke_excepthook
            self._invoke_excepthook = _make_invoke_excepthook()

        _dangling.add(self)

        # -------------------------------
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
        # -------------------------------
