__all__ = ["get_params", "safety_call", "safety_call_decorator"]

import asyncio
import inspect
from functools import wraps
from typing import Callable, Any, Awaitable, TypeVar, overload, Coroutine

T = TypeVar("T")


def get_params(fn: Callable, **params) -> tuple[tuple[Any, ...], dict[str, Any]]:
    args: list[Any] = []
    kwargs: dict[str, Any] = {}
    signature = inspect.signature(fn)
    positional_only = [
        param.name
        for param in signature.parameters.values()
        if param.kind == param.POSITIONAL_ONLY
    ]

    other = [
        param.name
        for param in signature.parameters.values()
        if param.name not in positional_only
    ]

    args_names = tuple(params.keys())

    for arg_name in positional_only:
        if arg_name in args_names:
            args.append(params[arg_name])

    for arg_name in other:
        if arg_name in args_names:
            kwargs[arg_name] = params[arg_name]

    return (tuple(args), kwargs)


@overload
async def safety_call(fn: Callable[..., Awaitable[T]], /, **params) -> T:
    pass


@overload
def safety_call(fn: Callable[..., T], /, **params) -> T:
    pass


def safety_call(fn: Callable[..., T], /, **params) -> T | Coroutine[Any, Any, T]:
    args, kwargs = get_params(fn, **params)

    if asyncio.iscoroutinefunction(fn):
        return fn(*args, **kwargs)
    else:
        return fn(*args, **kwargs)


if __name__ == "__main__":

    async def func(a, b, /, c=3) -> None:
        await asyncio.sleep(2)
        print(a, b, c)

    class A:
        @staticmethod
        def f(a, b, /, c):
            print(a)

    async def main() -> None:
        await safety_call(func, a=1, b=2)

    asyncio.run(main())


def safety_call_decorator(function: Callable[..., Awaitable[T]] | Callable[..., T]):

    @wraps(function)
    def wrapper(**kwargs):
        return safety_call(function, **kwargs)

    wrapper.__signature__ = inspect.signature(function)  # type: ignore
    return wrapper
