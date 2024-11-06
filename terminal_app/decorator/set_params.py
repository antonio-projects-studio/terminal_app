__all__ = ["set_params"]

import inspect
from functools import wraps
from typing import Any, Callable


def set_params(func: Callable[..., Any], args: list[tuple[Any, int]], **kwargs):
    @wraps
    def wrapper(*a, **kw):
        arguments = list(a)

        for arg in args:
            value, ind = arg
            arguments.insert(ind, value)

        kw.update(kwargs)

        return func(*arguments, **kw)

    setattr(wrapper, "__signature__", inspect.signature(func))
    return wrapper
