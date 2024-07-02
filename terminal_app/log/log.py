__all__ = ["register_logger", "LoggingMeta", "BaseLogging"]

import __main__
import logging
from typing import Any
from logging import Logger
from pathlib import Path
from inspect import getfile


def register_logger(path: Path | str, name: str | None = None) -> Logger:

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    file_path = Path(__main__.__file__).parent / path if isinstance(path, str) else path
    file_handler = logging.FileHandler(file_path.as_posix(), mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    name = name if name is not None else file_path.stem
    logger = logging.getLogger(f"{name}.Engine")
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    return logger


class LoggingMeta(type):
    logger: Logger
    root_logger: Logger

    def __new__(
        mcls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]
    ) -> type:
        cls = super().__new__(mcls, name, bases, namespace)

        if "BaseLogging" in [base.__name__ for base in bases]:
            cls.root_logger = register_logger(f"{name.lower()}.root.log")

        if namespace.get("LOGGING", None) is True:
            file = Path(getfile(cls))
            cls.logger = register_logger(file.parent / (file.stem + ".log"))

        return cls


class BaseLogging(metaclass=LoggingMeta):
    LOGGING = False
