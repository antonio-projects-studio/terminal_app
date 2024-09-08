__all__ = ["chunks"]

from typing import TypeVar

T = TypeVar("T")


def chunks(array: list[T], size: int) -> list[list[T]]:
    return [array[x : x + size] for x in range(0, len(array), size)]
