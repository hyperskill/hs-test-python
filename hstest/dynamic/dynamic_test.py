from __future__ import annotations

import inspect
from typing import Any

from hstest.stage_test import StageTest


def dynamic_test(
    func: Any | None = None,
    *,
    order: int | None = None,
    data: Any = None,
    time_limit: int | None = None,
    feedback: str | None = None,
    repeat: int = 1,
    files: dict[str, str] | None = None,
) -> Any:
    """Decorator for creating dynamic tests.

    Args:
        func: Function to decorate
        order: Order of test execution
        data: Test data
        time_limit: Time limit for test execution
        feedback: Custom feedback message for the test
        repeat: Number of times to repeat the test
        files: Dictionary of files to be created for the test

    Returns:
        DynamicTestingMethod: A decorated test method
    """

    class DynamicTestingMethod:
        def __init__(self, fn: Any) -> None:
            self.fn = fn

        def __set_name__(self, owner: StageTest, name: str) -> None:
            # do something with owner, i.e.
            # print(f"Decorating {self.fn} and using {owner}")  # noqa: ERA001
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
