"""Some useful tools"""
from pathlib import Path

from platformdirs import user_cache_dir

# Get the package path
PACKAGE_PATH = Path(user_cache_dir("tktermwidget"))
# Get the history file
HISTORY_FILE = PACKAGE_PATH / "history.txt"
# Get the json file (style)
JSON_FILE = PACKAGE_PATH / "styles.json"


def check():
    """Check files and create them if they don't exsit"""
    from json import dump

    # Check the "tktermwidget" is exsit
    if not PACKAGE_PATH.exists():
        PACKAGE_PATH.mkdir(parents=True)

    # Check that the history file exists
    if not (HISTORY_FILE).exists():
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            f.close()

    # Check that the json file exists
    if not (JSON_FILE).exists():
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            dump("{}", f)


check()
