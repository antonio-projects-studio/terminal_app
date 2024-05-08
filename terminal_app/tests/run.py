import sys
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.parent.as_posix())
print(sys.path)

from terminal_app.core import Colorize, Color

print(Colorize(Color.PURPLE).colorize_terminal_output(header="test", content="test"))
Colorize(Color.PURPLE).colorize_terminal_input(content="Enter prompt: ")