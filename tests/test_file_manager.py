from terminal_app.file_manager import FileManager
from magic_filter import MagicFilter
from pathlib import Path

F = MagicFilter()

fm = FileManager(Path(__file__).parent, formats="*", only_cnt=True)

print(fm.cnts)