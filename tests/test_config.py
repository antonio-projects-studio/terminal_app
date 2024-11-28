from terminal_app.env import source

source(".terminal.env")["ANY"]
source(".terminal_lol.env")["ANY"]
config = source(".terminal_ap.env")
print(config["LOL"])