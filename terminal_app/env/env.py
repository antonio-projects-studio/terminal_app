import __main__
import os
import sys
import platform

from pathlib import Path
from dotenv import load_dotenv

OS = platform.system().lower()

BASE_DIR = Path(__main__.__file__).parent.parent

CONFIG_DIR = BASE_DIR / "configs"
DATA_DIR = BASE_DIR / "data"
DEV_DIR = CONFIG_DIR / f"development"
PROD_DIR = CONFIG_DIR / f"production"

PYTHON_DIR = Path(__main__.__file__).parent

MODE = os.getenv("PROD") or "development"
CURRENT_DIR = DEV_DIR if MODE == "development" else PROD_DIR


for path in [CONFIG_DIR, DATA_DIR, DEV_DIR, PROD_DIR]:
    if not path.exists():
        os.mkdir(path)


def source(env_files: str | list[str]) -> dict[str, str]:
    # TODO ignore " in .env
    data: dict[str, str] = {}

    def _source(env_files: str) -> None:
        file_path = CURRENT_DIR / env_files
        if not file_path.exists():
            with open(file_path, "w"):
                pass
            print(f"Create {file_path}")
        else:
            load_dotenv(CURRENT_DIR / env_files)

    def load_variables(env_files: str) -> None:
        file_path = CURRENT_DIR / env_files
        with open(file_path) as f:
            for line in f.readlines():
                line = line.strip()
                if not line.startswith("#"):
                    name = line[: line.find("=")].strip().strip('"').strip("'")
                    arg = line[line.find("=") + 1 :].strip().strip('"').strip("'")
                    data[name] = arg

    if isinstance(env_files, str):
        _source(env_files)
        load_variables(env_files)

    else:
        for path in env_files:
            _source(path)
            load_variables(path)

    return data


RUN_MODE = sys.argv[-1]
