from __future__ import annotations

from threading import current_thread, Thread
from typing import Any, TYPE_CHECKING

from hstest.dynamic.security.thread_group import ThreadGroup

if TYPE_CHECKING:
    from collections.abc import Callable


class ThreadHandler:
    _group = None
    _old_init: Callable[[], Thread] | None = None

    @classmethod
    def install_thread_group(cls) -> None:
        if cls._old_init is None:
            cls._old_init = Thread.__init__
            Thread.__init__ = ThreadHandler.init
            cls._group = ThreadGroup("Main")
            current_thread()._group = cls._group  # noqa: SLF001

    @classmethod
    def uninstall_thread_group(cls) -> None:
        if cls._old_init is not None:
            Thread.__init__ = cls._old_init
            cls._old_init = None
            del current_thread()._group  # noqa: SLF001
            cls._group = None

    @staticmethod
    def init(
        self: Thread,  # noqa: PLW0211
        group: ThreadGroup | None = None,
        target: Callable[..., Any] | None = None,
        name: str | None = None,
        args: tuple[Any, ...] | None = (),
        kwargs: dict[str, Any] | None = None,
        *,
        daemon: bool | None = None,
    ) -> None:
        ThreadHandler._old_init(self, None, target, name, args, kwargs, daemon=daemon)

        # Custom addition to Thread class (implement thread groups)
        if group is not None:
            self._group = group
        else:
            curr = current_thread()

            if hasattr(curr, "_group"):
                self._group = curr._group  # noqa: SLF001
            else:
                self._group = ThreadGroup(self._name)

        self._group.add(self)
