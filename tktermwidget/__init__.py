"""__init__ of the tktermwidget package"""
from json import dump
from pathlib import Path

from platformdirs import user_cache_dir

from .style import *  # noqa: F401
from .tkterm import Terminal  # noqa: F401

# Think we should put checks when load.
PACKAGE_PATH = Path(user_cache_dir("tktermwidget"))  # Get the package path
HISTORY_FILE = PACKAGE_PATH / "history.txt"  # Get the history file
JSON_FILE = PACKAGE_PATH / "styles.json"  # Get the json file (style)

if not PACKAGE_PATH.exists():  # Check the "tktermwidget" is exsit
    PACKAGE_PATH.mkdir(parents=True)
    # Also create the history file
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.close()
    # Also create the json file
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        dump("{}", f)

# Check that the history file exists
if not (HISTORY_FILE).exists():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.close()

# Check that the json file exists
if not (JSON_FILE).exists():
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        dump("{}", f)
