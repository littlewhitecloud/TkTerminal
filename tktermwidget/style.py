"""Styles for terminal"""
import json
from platformdirs import user_cache_dir
from pathlib import Path

# Format:
# {yourstylename}: dict = {
#    "background": "{yourhexcolor}",        
#    "insertbackground": "{yourhexcolor}",
#    "selectbackground": "{yourhexcolor}",
#    "selectforeground": "{yourhexcolor}",
#    "foreground": "{yourhexcolor}",
# }

# Constants
STYLE_PATH = Path(user_cache_dir("tktermwidget"))
JSON_FILE = STYLE_PATH / "styles.json"

if not STYLE_PATH.exists():
    STYLE_PATH.mkdir(parents=True)
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        f.close()

if not (JSON_FILE).exists():
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        f.close()


# Built-in styles
Default: dict = {  # Style for normal tkterminalwidget
    "background": "#2B2B2B",
    "insertbackground": "#DCDCDC",
    "selectbackground": "#b4b3b3",
    "selectforeground": "#e6e6e6",
    "foreground": "#cccccc",
}

Powershell: dict = {  # Style for powershell
    "background": "#012456",
    "insertbackground": "#eeedf0",
    "selectbackground": "#fedba9",
    "selectforeground": "#11120f",
    "foreground": "#cccccc",
}

Command: dict = {  # Style for normal "cmd.exe"
    "background": "#000000",
    "insertbackground": "#f2f2f2",
    "selectbackground": "#f3f3f3",
    "selectforeground": "#000000",
    "foreground": "#f2f2f2",
}
# TODO: add a user custom style function later...

# Styles creater
def writestyle(**styles) -> None:
	with open(JSON_FILE, "w", encoding = "utf-8") as json_obj:
		json.dump(styles, json_obj)

def load_style() -> dict:
	with open(JSON_FILE, "r", encoding = "utf-8") as json_obj:
		return json.load(json_obj)

#writestyle(background = "#2B2B2B", insertbackground = "#DCDCDC", selectbackground = "#b4b3b3", selectforeground = "#e6e6e6", foreground = "#cccccc")

Custom: dict = load_style()
#print(Custom)
