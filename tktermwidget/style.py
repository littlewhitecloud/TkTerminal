"""Styles for terminal"""
import json
from pathlib import Path

from platformdirs import user_cache_dir

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

# Styles format:
# {yourstylename}: dict = {
#    "background": "{yourhexcolor}",
#    "insertbackground": "{yourhexcolor}",
#    "selectbackground": "{yourhexcolor}",
#    "selectforeground": "{yourhexcolor}",
#    "foreground": "{yourhexcolor}",
# }

# Styles creater
def writestyle(**styles) -> None:
    """Write the style into the json file"""
    # User can use this function to write with their own style
    # TODO: improve it, new style will overwrite the old style
    with open(JSON_FILE, "w", encoding="utf-8") as json_obj:
        json.dump(styles, json_obj)

def load_style() -> dict:
    """Get style from the json file"""
    # User also can use this function to get their own style
    with open(JSON_FILE, "r", encoding="utf-8") as json_obj:
        return json.load(json_obj)

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

Git: dict = {
    "background": "#000000",
    "insertbackground": "#bfbfbf",
    "selectbackground": "#bfbfbf",
    "selectforeground": "#0E0E0E",
    "foreground": "#efefef",
}

# User custom function
Custom: dict = load_style()

"""
writestyle(background = "#2B2B2B", insertbackground = "#DCDCDC", 
selectbackground = "#b4b3b3", selectforeground = "#e6e6e6", foreground = "#cccccc")
"""
