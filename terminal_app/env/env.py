__all__ = [
    "OS",
    "BASE_DIR",
    "WORK_DIR",
    "SSH_DIR",
    "CONFIG_BASE_DIR",
    "DATA_DIR",
    "DEV_DIR",
    "PROD_DIR",
    "APP_MODE",
    "RUN_MODE",
    "CONFIG_DIR",
    "source",
]


import __main__
import os
import sys
import platform

from pathlib import Path
from dotenv import load_dotenv
from pytest_is_running import is_running


OS = platform.system().lower()

if is_running():
    BASE_DIR = Path(os.getcwd()) / "tests"
else:
    BASE_DIR = (
        Path(os.getcwd()).parent if "-m" not in sys.orig_argv else Path(os.getcwd())
    )

WORK_DIR = (
    Path(os.getcwd())
    if "-m" not in sys.orig_argv
    else Path(os.path.dirname(__main__.__file__))
)
CONFIG_BASE_DIR = BASE_DIR / "configs"
tmp = os.getenv("DATA_DIR")
DATA_DIR = (BASE_DIR / "data") if not tmp else Path(tmp)
tmp = os.getenv("SSH_DIR")
SSH_DIR = (BASE_DIR / ".ssh") if not tmp else Path(tmp)

tmp = os.getenv("CONFIG_PATH")
CONFIG_PATH = (CONFIG_BASE_DIR / tmp) if tmp else None
DEV_DIR = CONFIG_BASE_DIR / "development"
PROD_DIR = CONFIG_BASE_DIR / "production"

APP_MODE = os.getenv("PROD") or "development"
RUN_MODE = sys.argv[-1]

CONFIG_DIR = (
    Path(CONFIG_PATH)
    if CONFIG_PATH
    else DEV_DIR if APP_MODE == "development" else PROD_DIR
)

if os.getenv("INIT_DEFAULT"):
    for path in [CONFIG_BASE_DIR, DATA_DIR, DEV_DIR, PROD_DIR, SSH_DIR]:
        if not path.exists():
            os.mkdir(path)

print("Project config:")
print(f"{OS=}")
print(f"{BASE_DIR=}")
print(f"{WORK_DIR=}")
print(f"{CONFIG_DIR=}")
print(f"{DATA_DIR=}")
print(f"{SSH_DIR=}")
print(f"{APP_MODE=}")


def source(env_files: str | list[str]) -> dict[str, str]:
    # TODO ignore " in .env
    data: dict[str, str] = {}

    def _source(env_files: str) -> None:
        assert env_files.endswith(".env"), "The configuration file must end in .env"
        file_path = CONFIG_DIR / env_files
        if not file_path.exists():
            with open(file_path, "w"):
                pass
            print(f"Create {file_path}")
        else:
            load_dotenv(CONFIG_DIR / env_files)

    def load_variables(env_files: str) -> None:
        file_path = CONFIG_DIR / env_files
        with open(file_path) as f:
            for line in f.readlines():
                line = line.strip()
                if not line.startswith("#"):
                    name = line[: line.find("=")].strip().strip('"').strip("'")
                    arg = line[line.find("=") + 1 :].strip().strip('"').strip("'")
                    data[name] = os.getenv(name, "")

    if isinstance(env_files, str):
        _source(env_files)
        load_variables(env_files)

    else:
        for path in env_files:
            _source(path)
            load_variables(path)

    return data
