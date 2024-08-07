from __future__ import annotations

__all__ = ["register_logger", "LoggingMeta", "RootLogging"]

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
    library: bool = False,
    level: logging._Level = logging.DEBUG,
) -> Logger:

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    if path is not None:

        file_path = RootLogging.root_path / path if isinstance(path, str) else path

    name = name if name is not None else file_path.stem if path is not None else None

    if name in logging.Logger.manager.loggerDict.keys() or library:
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
        file_handler = logging.FileHandler(file_path.as_posix(), mode="w")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    logger.setLevel(level)

    return logger


class LoggingMeta(type):
    __folder_name__: str = "logging"
    __root_path__: Path = Path(__main__.__file__).parent.parent / __folder_name__
    logger: Logger
    root_logger: Logger

    @property
    def root_path(cls) -> Path:
        create_folder = False
        create_folder = not LoggingMeta.__root_path__.exists()
        create_folder = not LoggingMeta.__root_path__.is_dir()
        if create_folder:
            os.mkdir(LoggingMeta.__root_path__)

        return LoggingMeta.__root_path__

    def __new__(
        mcls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]
    ) -> type:
        cls = super().__new__(mcls, name, bases, namespace)

        if "RootLogging" in [base.__name__ for base in bases]:
            if os.getenv(f"{name}_LOGGING"):

                cls.root_logger = register_logger(cls.root_path / f"{name}.log")

        if namespace.get("LOGGING", None) is True:
            file = Path(getfile(cls))
            cls.logger = register_logger(file.parent / (file.stem + ".log"), name=name)

        return cls


class RootLogging(metaclass=LoggingMeta):
    LOGGING = False
