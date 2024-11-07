__all__ = ["get_params", "safety_call"]

import asyncio
import inspect
from functools import wraps
from collections.abc import Mapping
from typing import Callable, Any, Awaitable, TypeVar, overload, Coroutine

T = TypeVar("T")


def get_params(
    fn: Callable, /, params: Mapping[str, Any]
) -> tuple[tuple[Any, ...], dict[str, Any]]:
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
def safety_call(fn: Callable[..., Awaitable[T]], /) -> Callable[..., Awaitable[T]]:
    pass


@overload
def safety_call(fn: Callable[..., T], /) -> Callable[..., T]:
    pass


@overload
async def safety_call(
    fn: Callable[..., Awaitable[T]], /, params: Mapping[str, Any]
) -> T:
    pass


@overload
def safety_call(fn: Callable[..., T], /, params: Mapping[str, Any]) -> T:
    pass


def safety_call(
    fn: Callable[..., T], /, params: Mapping[str, Any] | None = None
) -> T | Coroutine | Callable[..., T]:
    if params is None:

        @wraps(fn)
        def wrapper(**kwargs):

            return safety_call(fn, params=kwargs)

        setattr(wrapper, "__signature__", inspect.signature(fn))
        return wrapper

    args, kwargs = get_params(fn, params)

    if asyncio.iscoroutinefunction(fn):
        return fn(*args, **kwargs)
    else:
        return fn(*args, **kwargs)
