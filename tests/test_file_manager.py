from terminal_app.file_manager import FileManager
from magic_filter import MagicFilter
from pathlib import Path

F = MagicFilter()

fm = FileManager(Path(__file__).parent / "data", formats=["json"])

print(fm.paths)
print(fm.cnt)

fm.copy(Path(__file__).parent / "data_copy")