__all__ = ["FileManager"]

import shutil
from pathlib import Path
from typing import Literal
from magic_filter import MagicFilter
from terminal_app.naming import generate_path


class FileManager:

    @property
    def cnt(self) -> int:
        return len(self.paths)

    def __init__(
        self,
        root: Path,
        formats: list[str] | Literal["*"] = "*",
        filter: MagicFilter | None = None,
    ) -> None:

        self.root = root
        self.formats = formats
        self.filter = filter
        self.paths = []

        assert self.root.is_dir()

        self.paths = self.get_files(self.root, self.formats, self.filter)

    @staticmethod
    def get_files(
        dir: Path,
        formats: list[str] | Literal["*"] = "*",
        filter: MagicFilter | None = None,
    ) -> list[Path]:
        paths: list[Path] = []

        for item in dir.iterdir():
            if item.is_dir():
                paths += FileManager.get_files(item, formats, filter)
            else:
                suffix = item.suffix.strip(".")
                if (suffix in set(formats) or "*" in formats) and (
                    filter is None or filter.resolve(item)
                ):
                    paths.append(item)

        return paths
    
    def copy(self, path: Path, filter: MagicFilter | None = None) -> None:
        
        path.mkdir(exist_ok=True)
        
        for file in self.paths:
            if filter is None or filter.resolve(file):
                shutil.copyfile(file, generate_path(path / file.name))
            
