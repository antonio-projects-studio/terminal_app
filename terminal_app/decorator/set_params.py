__all__ = ["set_params"]

import inspect
from functools import wraps
from typing import Any, Callable


def set_params(
    args: tuple[tuple[Any, int], ...] = (), kwargs: dict[str, Any] | None = None
):

    def decorator(func: Callable[..., Any]):

        @wraps(func)
        def wrapper(*a, **kw):
            arguments = list(a)

            for arg in args:
                value, ind = arg
                arguments.insert(ind, value)

            if kwargs is not None:
                kw.update(kwargs)

            return func(*arguments, **kw)

        setattr(wrapper, "__signature__", inspect.signature(func))
        return wrapper

    return decorator
