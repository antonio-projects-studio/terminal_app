import __main__
import os
import sys
import platform

from typing import Any
from pathlib import Path
from dotenv import load_dotenv

OS = platform.system().lower()

BASE_DIR = Path(__main__.__file__).parent.parent
CONFIG_DIR = BASE_DIR / "configs"
DEV_OS_DIR = CONFIG_DIR / f"development_{OS}"

PYTHON_DIR = Path(__main__.__file__).parent

MODE = os.getenv("MODE") or "development"

if not CONFIG_DIR.exists():
    os.mkdir(CONFIG_DIR)

if not DEV_OS_DIR.exists():
    os.mkdir(DEV_OS_DIR)


def source(env_files: str | list[str]) -> dict[str, str]:
    data: dict[str, str] = {}

    def _source(env_files: str) -> None:
        file_path = DEV_OS_DIR / env_files
        if not file_path.exists():
            with open(file_path, "w"):
                pass
            print(f"Create {file_path}")
        else:
            load_dotenv(DEV_OS_DIR / env_files)

    def load_variables(env_files: str) -> None:
        file_path = DEV_OS_DIR / env_files
        with open(file_path) as f:
            for line in f.readlines():
                line = line.strip()
                if not line.startswith("#"):
                    name = line[: line.find("=")].strip()
                    arg = line[line.find("=") + 1 :].strip()
                    data[name] = arg

    if MODE == "development":
        if isinstance(env_files, str):
            _source(env_files)
            load_variables(env_files)

        else:
            for path in env_files:
                _source(path)
                load_variables(path)

    return data


RUN_MODE = sys.argv[-1]
