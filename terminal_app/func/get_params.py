__all__ = ["get_params"]

from typing import Callable, Any


def get_params(fn: Callable, **kw) -> tuple[tuple[Any, ...], dict[str, Any]]:
    args: list[Any] = []
    kwargs: dict[str, Any] = {}
    args_names = fn.__code__.co_varnames
    positional_only = args_names[: fn.__code__.co_posonlyargcount]
    other = args_names[fn.__code__.co_posonlyargcount :]

    args_names = tuple(kw.keys())

    for arg_name in positional_only:
        if arg_name in args_names:
            args.append(kw[arg_name])

    for arg_name in other:
        if arg_name in args_names:
            kwargs[arg_name] = kw[arg_name]

    return (tuple(args), kwargs)
