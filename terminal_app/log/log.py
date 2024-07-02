from __future__ import annotations

__all__ = ["register_logger", "LoggingMeta", "BaseLogging"]

import __main__
import os
import logging
from typing import Any
from logging import Logger
from pathlib import Path
from inspect import getfile

suffix = "terminal_app.Engine"


def register_logger(
    path: Path | str | None = None,
    name: str | None = None,
    level: logging._Level = logging.DEBUG,
) -> Logger:

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    if path is not None:

        file_path = (
            Path(__main__.__file__).parent / path if isinstance(path, str) else path
        )
        file_handler = logging.FileHandler(file_path.as_posix(), mode="w")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

    name = name if name is not None else file_path.stem if path is not None else None

    if name in logging.Logger.manager.loggerDict.keys():
        print(f"Change {name} logger")
        logger = logging.getLogger(name)
        for handler in logger.handlers:
            logger.removeHandler(handler)
    else:
        if name is not None:
            assert (
                f"{name}.{suffix}" not in logging.Logger.manager.loggerDict.keys()
            ), "The same name of the loggers"
            logger = logging.getLogger(f"{name}.{suffix}")
        else:
            logger = logging.getLogger(suffix)

    if path is not None:
        logger.addHandler(file_handler)
    else:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    logger.setLevel(level)

    return logger


class LoggingMeta(type):
    __folder_name__: str = "loggers"
    __root_path__: Path = Path(__main__.__file__).parent / __folder_name__
    logger: Logger
    root_logger: Logger

    def __new__(
        mcls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]
    ) -> type:
        cls = super().__new__(mcls, name, bases, namespace)

        if "BaseLogging" in [base.__name__ for base in bases]:

            create_folder = False
            create_folder = not cls.__root_path__.exists()
            create_folder = not cls.__root_path__.is_dir()
            if create_folder:
                os.mkdir(cls.__root_path__)

            cls.root_logger = register_logger(
                cls.__root_path__ / f"{name.lower()}_root.log"
            )

        if namespace.get("LOGGING", None) is True:
            file = Path(getfile(cls))
            cls.logger = register_logger(file.parent / (file.stem + ".log"))

        return cls


class BaseLogging(metaclass=LoggingMeta):
    LOGGING = False
