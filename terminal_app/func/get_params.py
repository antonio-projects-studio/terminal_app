__all__ = ["get_params", "safety_call"]

import asyncio
from typing import Callable, Any, Awaitable, TypeVar, overload, Coroutine

T = TypeVar("T")


def get_params(fn: Callable, **params) -> tuple[tuple[Any, ...], dict[str, Any]]:
    args: list[Any] = []
    kwargs: dict[str, Any] = {}
    args_names = fn.__code__.co_varnames
    positional_only = args_names[: fn.__code__.co_posonlyargcount]
    other = args_names[fn.__code__.co_posonlyargcount :]

    args_names = tuple(params.keys())

    for arg_name in positional_only:
        if arg_name in args_names:
            args.append(params[arg_name])

    for arg_name in other:
        if arg_name in args_names:
            kwargs[arg_name] = params[arg_name]

    return (tuple(args), kwargs)


@overload
async def safety_call(fn: Callable[..., Awaitable[T]], **params) -> T:
    pass


@overload
def safety_call(fn: Callable[..., T], **params) -> T:
    pass


def safety_call(fn: Callable[..., T], **params) -> T | Coroutine[Any, Any, T]:
    args, kwargs = get_params(fn, **params)

    if asyncio.iscoroutinefunction(fn):
        return fn(*args, **kwargs)
    else:
        return fn(*args, **kwargs)


if __name__ == "__main__":

    async def func(a, b, c=3) -> None:
        await asyncio.sleep(2)
        print(a, b, c)

    async def main() -> None:
        await safety_call(func, a=1, b=2)

    asyncio.run(main())
