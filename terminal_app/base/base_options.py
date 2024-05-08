from enum import Enum
from typing import Any, Callable
import sys


class BaseOptions(Enum):
    def __init__(self, command: str, func: Callable[..., bool | list[str]] | None = None) -> None:
        self.command = command
        self.func = func

    def __str__(self) -> str:
        return (
            " ".join(str(self.name).lower().capitalize().split("_"))
            + f" ({self.command})"
        )

    def execute(self, command: str, **kwargs) -> Any | None:
        if command == self.command:
            if not self.func:
                return

            return self.func(**kwargs)

    @classmethod
    @property
    def present(cls) -> str:
        result: str = ""
        for ind, opt in enumerate(cls):
            result += f"{ind + 1}. {opt}\n"

        return result
