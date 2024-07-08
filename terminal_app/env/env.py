import os
import sys

from pathlib import Path
from dotenv import load_dotenv
import platform
import __main__

OS = platform.system().lower()

BASE_DIR = Path(__main__.__file__).parent.parent
CONFIG_DIR = BASE_DIR / "configs"
DEV_OS_DIR = CONFIG_DIR / "development_{OS}"

PYTHON_DIR = Path(__main__.__file__).parent


MODE = os.getenv("MODE") or "development"

if not CONFIG_DIR.exists():
    os.mkdir(CONFIG_DIR)

if not DEV_OS_DIR.exists():
    os.mkdir(DEV_OS_DIR)


def source(env_files: str | list[str]) -> None:
    if MODE == "development":
        if isinstance(env_files, str):
            load_dotenv(DEV_OS_DIR / env_files)

        else:
            for path in env_files:
                load_dotenv(DEV_OS_DIR / path)


RUN_MODE = sys.argv[-1]
