from __future__ import annotations

import inspect
from typing import Any

from hstest.stage_test import StageTest
from hstest.test_case.test_case import DEFAULT_TIME_LIMIT


def dynamic_test(
    func=None,
    *,
    order: int = 0,
    time_limit: int = DEFAULT_TIME_LIMIT,
    data: list[Any] | None = None,
    feedback: str = "",
    repeat: int = 1,
    files: dict[str, str] | None = None,
):
    """Decorator for creating dynamic tests."""

    class DynamicTestingMethod:
        def __init__(self, fn) -> None:
            self.fn = fn

        def __set_name__(self, owner, name):
            # do something with owner, i.e.
            # print(f"Decorating {self.fn} and using {owner}")
            self.fn.class_name = owner.__name__

            # then replace ourself with the original method
            setattr(owner, name, self.fn)

            if not issubclass(owner, StageTest):
                return

            from hstest.dynamic.input.dynamic_testing import DynamicTestElement

            methods: list[DynamicTestElement] = owner.dynamic_methods()
            methods += [
                DynamicTestElement(
                    test=self.fn,
                    name=self.fn.__name__,
                    order=(order, len(methods)),
                    repeat=repeat,
                    time_limit=time_limit,
                    feedback=feedback,
                    data=data,
                    files=files,
                )
            ]

    is_method = inspect.ismethod(func)
    is_func = inspect.isfunction(func)
    if is_method or is_func:
        # in case it is called as @dynamic_test
        return DynamicTestingMethod(func)

    # in case it is called as @dynamic_test(...)
    return DynamicTestingMethod
