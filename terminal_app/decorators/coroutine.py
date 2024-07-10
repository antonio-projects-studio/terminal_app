from functools import wraps


def coroutine(func):
    @wraps(func)
    def wrapper_coroutine(*args, **kwargs):
        f = func(*args, **kwargs)
        next(f)
        return f

    return wrapper_coroutine
