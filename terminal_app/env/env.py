__all__ = [
    "OS",
    "BASE_DIR",
    "WORK_DIR",
    "SSH_DIR",
    "MEDIA_DIR",
    "DATA_DIR",
    "RUN_MODE",
    "PROJECT_CONFIG",
    "source",
]


import __main__
import os
import sys
import platform

from pathlib import Path
from dotenv import load_dotenv
from argparse import ArgumentParser
from typing import Any, Self, Literal

from tabulate import tabulate
from pytest_is_running import is_running
from pydantic import BaseModel, model_validator, Field


parser = ArgumentParser()
parser.add_argument("-cf", "--config", type=str, default="development")
args, _ = parser.parse_known_args()

OS = platform.system().lower()
RUN_MODE: Literal["script", "module", "jupyter", "bin"]

try:
    __main__.__file__
    if "-m" in sys.orig_argv:
        RUN_MODE = "module"
    elif sys.argv[0].endswith(".py"):
        RUN_MODE = "script"

    else:
        RUN_MODE = "bin"
except:
    RUN_MODE = "jupyter"


match RUN_MODE:
    case "script":
        BASE_DIR = WORK_DIR = Path(os.path.dirname(__main__.__file__))
    case "module":
        WORK_DIR = Path(os.path.dirname(__main__.__file__))
        BASE_DIR = WORK_DIR.parent
    case "bin":
        WORK_DIR = Path(os.getcwd())
        BASE_DIR = WORK_DIR.parent

        if is_running():
            BASE_DIR = Path(os.getcwd()) / "tests"
    case "jupyter":
        BASE_DIR = WORK_DIR = Path(os.getcwd())

if (tmp := os.getenv("BASE_DIR")) is not None:
    BASE_DIR = Path(tmp)

if (tmp := os.getenv("WORK_DIR")) is not None:
    WORK_DIR = Path(tmp)

CONFIG_NAME = ".terminal_app.env"
CONFIG_FILE = BASE_DIR / CONFIG_NAME


class ProjectConfig(BaseModel):
    BASE_DIR: Path = BASE_DIR
    WORK_DIR: Path = WORK_DIR
    CONFIGS_DIR: Path = BASE_DIR / "configs"
    DEV_DIR: Path = CONFIGS_DIR / "development"
    PROD_DIR: Path = CONFIGS_DIR / "production"
    TEST_DIR: Path = CONFIGS_DIR / "test"
    CERTIFICATES_DIR: Path = BASE_DIR / "certificates"
    SSH_DIR: Path = CERTIFICATES_DIR / "ssh"
    DATA_DIR: Path = BASE_DIR / "data"
    MEDIA_DIR: Path = DATA_DIR / "media"
    DOCUMENT_DIR: Path = MEDIA_DIR / "document"
    VIDEO_DIR: Path = MEDIA_DIR / "video"
    PHOTO_DIR: Path = MEDIA_DIR / "photo"

    INIT_FOLDERS: bool = False
    DESCRIPTION: str = Field(init=False, exclude=True)

    @property
    def OS(self) -> str:
        return OS

    @property
    def RUN_MODE(self) -> str:
        return RUN_MODE

    @property
    def CONFIG_DIR(self) -> Path:
        return self.CONFIGS_DIR / args.config

    @model_validator(mode="before")
    @classmethod
    def init_project(cls, data: dict[str, Any]) -> dict[str, Any]:
        if not CONFIG_FILE.exists():
            with open(CONFIG_FILE, "w") as f:
                f.write(f"# {CONFIG_FILE.name}\n")

            print(f"Create {CONFIG_FILE}")

        ProjectConfig.check_env_file(CONFIG_FILE)

        desc = f"# Terminal App\n- OS: {OS}\n- CONFIG: {args.config}\n- RUN_MODE: {RUN_MODE}\n{_show_env_info(CONFIG_FILE)}"

        data = source(CONFIG_FILE)
        data["INIT_FOLDERS"] = data["INIT_FOLDERS"].lower()
        data["DESCRIPTION"] = desc

        return data

    @classmethod
    def check_env_file(cls, env_file_path: Path) -> None:
        keys = _parse_env_file(env_file_path).keys()
        with open(env_file_path, "a") as f:
            for field, info in cls.model_fields.items():
                if field not in keys and not info.exclude:
                    f.write(f"{field}={info.default}\n")

    @model_validator(mode="after")
    def check_init_folders(self) -> Self:
        if self.INIT_FOLDERS:
            for _, path in self:
                if isinstance(path, Path):
                    if not path.exists():
                        os.mkdir(path)

        another = ""
        for env_file in self.CONFIG_DIR.iterdir():
            another += f"\n# {env_file.stem.replace("_", " ").strip(".").title()}\n"
            another += _show_env_info(env_file)

        self.DESCRIPTION += another

        return self

    def __repr__(self) -> str:
        return self.DESCRIPTION


def _parse_env_file(env_file_path: Path) -> dict[str, Any]:
    data = {}
    with open(env_file_path) as f:
        for line in f.readlines():
            line = line.strip()
            if not line.startswith("#") and line:
                name = line[: line.find("=")].strip().strip('"').strip("'")
                arg = line[line.find("=") + 1 :].strip().strip('"').strip("'")
                data[name] = arg

    return data


def _show_env_info(env_file_path: Path) -> str:
    columns = ["name", "env", "file"]
    rows = []

    for name, file in _parse_env_file(env_file_path).items():
        rows.append((name, os.getenv(name), file))

    return tabulate(rows, headers=columns, tablefmt="psql")


def source(env_files: str | list[str] | Path | list[Path]) -> dict[str, str]:
    data: dict[str, str] = {}
    assert (
        env_files != CONFIG_NAME
    ), f"The env file cannot be assigned the name  {CONFIG_NAME}"

    def _get_path(env_file: str) -> Path:
        config_path = PROJECT_CONFIG.CONFIG_DIR

        return config_path / env_file

    def _source(env_file_path: Path) -> None:
        assert env_file_path.name.endswith(
            ".env"
        ), "The configuration file must end in .env"

        if not env_file_path.exists():
            with open(env_file_path, "w") as f:
                f.write(f"# {env_file_path.name}\n")

            print(f"Create {env_file_path}")

        load_dotenv(env_file_path)

    def load_variables(env_file_path: Path) -> None:
        keys = _parse_env_file(env_file_path).keys()
        for key in keys:
            data[key] = os.getenv(key, "")

    if isinstance(env_files, str | Path):
        if isinstance(env_files, Path):
            path = env_files
        else:
            path = _get_path(env_files)
        _source(path)
        load_variables(path)

    else:
        for env_file in env_files:
            if isinstance(env_file, Path):
                path = env_file
            else:
                path = _get_path(env_file)
            _source(path)
            load_variables(path)

    return data


PROJECT_CONFIG = ProjectConfig()
print(PROJECT_CONFIG)
DATA_DIR = PROJECT_CONFIG.DATA_DIR
SSH_DIR = PROJECT_CONFIG.SSH_DIR
MEDIA_DIR = PROJECT_CONFIG.MEDIA_DIR
