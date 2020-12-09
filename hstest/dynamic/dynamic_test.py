import inspect

from hstest.stage_test import StageTest


def dynamic_test(*args):
    """
    Decorator for creating dynamic tests
    """

    class DynamicTestingMethod:
        def __init__(self, fn):
            self.fn = fn

        def __set_name__(self, owner, name):
            # do something with owner, i.e.
            print(f"Decorating {self.fn} and using {owner}")
            self.fn.class_name = owner.__name__

            if not issubclass(owner, StageTest):
                setattr(owner, name, self.fn)
                return

            def decorator(*args, **kwargs):
                # print('Before')
                res = self.fn(*args, **kwargs)
                # print('After')
                return res

            # then replace ourself with the original method
            setattr(owner, name, self.fn)

            methods = owner._dynamic_methods.get(owner, [])
            methods += [decorator]
            owner._dynamic_methods[owner] = methods

    if len(args) == 0:
        return DynamicTestingMethod

    is_method = inspect.ismethod(args[0])
    is_func = inspect.isfunction(args[0])
    if len(args) == 1 and (is_method or is_func):
        return DynamicTestingMethod(args[0])

    return DynamicTestingMethod
