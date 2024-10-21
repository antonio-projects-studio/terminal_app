__all__ = ["FileManager"]

import shutil
from pathlib import Path
from typing import Literal, overload
from magic_filter import MagicFilter
from terminal_app.naming import generate_path
from collections import defaultdict


class FileManager:

    def __init__(
        self,
        root: Path,
        formats: list[str] | Literal["*"] = "*",
        filter: MagicFilter | None = None,
        only_cnt: bool = False
    ) -> None:

        self.root = root
        self.formats = formats
        self.filter = filter
        self.paths: dict[str, list[Path]] = {}

        assert self.root.is_dir()
        
        if not only_cnt:
            self.paths = self.get_files(self.root, self.formats, self.filter)
        else:
            self.cnts = self.get_files(self.root, self.formats, self.filter, only_cnt)

    @overload
    @staticmethod
    def get_files(
        dir: Path,
        formats: list[str] | Literal["*"] = "*",
        filter: MagicFilter | None = None,
    ) -> dict[str, list[Path]]:
        pass
    
    @overload
    @staticmethod
    def get_files(
        dir: Path,
        formats: list[str] | Literal["*"] = "*",
        filter: MagicFilter | None = None,
        only_cnt: Literal[True] = True
    ) -> dict[str, int]:
        pass
    
    @staticmethod
    def get_files(
        dir: Path,
        formats: list[str] | Literal["*"] = "*",
        filter: MagicFilter | None = None,
        only_cnt: bool = False,
    ) -> dict[str, list[Path]] | dict[str, int]:

        if not only_cnt:
            paths: dict[str, list[Path]] = defaultdict(lambda: [])
        else:
            cnts: dict[str, int] = defaultdict(lambda: 0)

        for item in dir.iterdir():
            if item.is_dir():
                if only_cnt:
                    for format, cnt in FileManager.get_files(item, formats, filter, only_cnt).items(): # type: ignore
                        cnts[format] += cnt
                else:
                    for format, path in FileManager.get_files(item, formats, filter).items(): # type: ignore
                        paths[format] += path 
            else:
                suffix = item.suffix.strip(".")
                if (suffix in set(formats) or "*" in formats) and (
                    filter is None or filter.resolve(item)
                ):
                    if only_cnt:
                        cnts[suffix] += 1
                    else:
                        paths[suffix].append(item)
                        
        if only_cnt:
            return dict(cnts)

        return dict(paths)
    
    def copy(self, path: Path, formats: list[str] | Literal["*"] = "*", filter: MagicFilter | None = None) -> None:
        
        path.mkdir(exist_ok=True)
        
        for format, files in self.paths.items():
            if not (format in set(formats) or "*" in formats):
                continue
            for file in files:
                if filter is None or filter.resolve(file):
                    shutil.copyfile(file, generate_path(path / file.name))
            
