"""Some useful tools"""


def check():
    """Check files and create them if they don't exsit"""
    from json import dump
    from pathlib import Path

    from platformdirs import user_cache_dir

    # Get the package path
    PACKAGE_PATH = Path(user_cache_dir("tktermwidget"))
    # Get the history file
    HISTORY_FILE = PACKAGE_PATH / "history.txt"
    # Get the json file (style)
    JSON_FILE = PACKAGE_PATH / "styles.json"

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
