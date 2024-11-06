__all__ = ["set_params"]

import inspect
from typing import Any, Callable
from functools import wraps


def set_params(function: Callable, args: list[tuple[Any, int]], **kwargs):
    @wraps
    def wrapper(*a, **kw):
        arguments = list(a)

        for arg in args:
            value, ind = arg
            arguments.insert(ind, value)

        kw.update(kwargs)

        return function(*arguments, **kw)

    setattr(wrapper, "__signature__", inspect.signature(function))
    return wrapper
