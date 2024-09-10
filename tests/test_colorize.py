import _settings

from terminal_app.core import Colorize, Color

print(Colorize(Color.PURPLE).colorize_terminal_output(header="test", content="test"))
Colorize(Color.PURPLE).colorize_terminal_input(content="Enter prompt: ")


