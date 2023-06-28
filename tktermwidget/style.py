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


# Styles creater
def write_style(**styles) -> None:
    """Write the style into the json file"""
    # User can use this function to write with their own style
    # TODO: improve it, new style will overwrite the old style
    with open(JSON_FILE, "w", encoding="utf-8") as json_obj:
        json.dump(styles, json_obj, indent=1)


def load_style() -> dict:
    """Get style from the json file"""
    # User also can use this function to get their own style
    with open(JSON_FILE, "r", encoding="utf-8") as json_obj:
        return json.load(json_obj)


def config_style() -> None:
    """Config the style with the ui"""
    # TODO: improve the code
    # TODO: improve the ui
    # TODO: fix some logic bug
    # TODO: ...
    from tkinter import Text, Tk
    from tkinter.colorchooser import askcolor
    from tkinter.ttk import Button, Entry, Frame, Label

    def selectcolor(entry: Entry, name: str) -> None:
        color = askcolor()[-1]
        entry.delete(0, "end")
        entry.insert("insert", color)
        style[name] = color
        renderupdate()

    def renderupdate() -> None:
        render.config(
            background=style["background"],
            insertbackground=style["insertbackground"],
            selectbackground=style["selectbackground"],
            selectforeground=style["selectforeground"],
            foreground=style["foreground"],
        )
        render.tag_config("select", background=style["selectbackground"], foreground=style["selectforeground"])
        config.update()

    def savestyle() -> None:
        write_style(
            background=style["background"],
            insertbackground=style["insertbackground"],
            selectbackground=style["selectbackground"],
            selectforeground=style["selectforeground"],
            foreground=style["foreground"],
        )
        config.destroy()

    config = Tk()
    config.geometry("825x500")
    config.title("Config your style")

    try:
        from sv_ttk import set_theme
    except:
        pass
    else:
        set_theme("light")
        config.option_add("*font", ("Cascadia Mono", 9))

    style: dict[str, str, str, str, str] = load_style()

    create = Label(config, text="Create your custom style!")

    backgroundframe = Frame(config)
    background = Label(backgroundframe, text="Choose or input your background hex color")
    backgroundentry = Entry(backgroundframe)
    backgroundbutton = Button(
        backgroundframe, text="...", width=3, command=lambda: selectcolor(backgroundentry, "background")
    )

    insertbackgroundframe = Frame(config)
    insertbackground = Label(insertbackgroundframe, text="Choose or input your insertbackground hex color")
    insertbackgroundentry = Entry(insertbackgroundframe)
    insertbackgroundbutton = Button(
        insertbackgroundframe, text="...", width=3, command=lambda: selectcolor(insertbackgroundentry, "insertbackground")
    )

    selectbackgroundframe = Frame(config)
    selectbackground = Label(selectbackgroundframe, text="Choose or input your selectbackground hex color")
    selectbackgroundentry = Entry(selectbackgroundframe)
    selectbackgroundbutton = Button(
        selectbackgroundframe, text="...", width=3, command=lambda: selectcolor(selectbackgroundentry, "selectbackground")
    )

    selectforegroundframe = Frame(config)
    selectforeground = Label(selectforegroundframe, text="Choose or input your selectforeground hex color")
    selectforegroundentry = Entry(selectforegroundframe)
    selectforegroundbutton = Button(
        selectforegroundframe, text="...", width=3, command=lambda: selectcolor(selectforegroundentry, "selectforeground")
    )

    foregroundframe = Frame(config)
    foreground = Label(foregroundframe, text="Choose or input your selectforeground hex color")
    foregroundentry = Entry(foregroundframe)
    foregroundbutton = Button(
        foregroundframe, text="...", width=3, command=lambda: selectcolor(foregroundentry, "foreground")
    )

    save = Button(config, text="Save", command=savestyle)
    cancel = Button(config, text="Cancel", command=config.destroy)

    # TODO: Add buttons and labels to help user to config the style
    render = Text(
        config,
        width=40,
        background=style["background"],
        insertbackground=style["insertbackground"],
        selectbackground=style["selectbackground"],
        selectforeground=style["selectforeground"],
        foreground=style["foreground"],
        font=("Cascadia Mono", 9, "normal"),
    )

    # TODO: Improve here
    render.insert("insert", "This is a normal text for test style.")
    render.tag_add("select", "1.31", "1.36")
    render.tag_config("select", background=style["selectbackground"], foreground=style["selectforeground"])
    render["state"] = "disable"

    render.pack(side="right", fill="y")
    create.pack(side="top", fill="y", pady=15)

    background.pack(side="left", fill="y")
    backgroundentry.pack(side="left")
    backgroundbutton.pack(side="left")
    backgroundframe.pack(side="top", fill="y")

    insertbackground.pack(side="left", fill="y")
    insertbackgroundentry.pack(side="left")
    insertbackgroundbutton.pack(side="left")
    insertbackgroundframe.pack(side="top", fill="y")

    selectbackground.pack(side="left", fill="y")
    selectbackgroundentry.pack(side="left")
    selectbackgroundbutton.pack(side="left")
    selectbackgroundframe.pack(side="top", fill="y")

    selectforeground.pack(side="left", fill="y")
    selectforegroundentry.pack(side="left")
    selectforegroundbutton.pack(side="left")
    selectforegroundframe.pack(side="top", fill="y")

    foreground.pack(side="left", fill="y")
    foregroundentry.pack(side="left")
    foregroundbutton.pack(side="left")
    foregroundframe.pack(side="top", fill="y")

    save.pack(side="bottom", fill="x")
    cancel.pack(side="bottom", fill="x")

    config.mainloop()


# Styles format:
# {yourstylename}: dict[str, str, str, str, str] = {
#    "background": "{yourhexcolor}",
#    "insertbackground": "{yourhexcolor}",
#    "selectbackground": "{yourhexcolor}",
#    "selectforeground": "{yourhexcolor}",
#    "foreground": "{yourhexcolor}",
# }

# Built-in styles
DEFAULT: dict[str, str, str, str, str] = {  # Style for normal tkterminalwidget
    "background": "#2B2B2B",
    "insertbackground": "#DCDCDC",
    "selectbackground": "#b4b3b3",
    "selectforeground": "#e6e6e6",
    "foreground": "#cccccc",
}

POWERSHELL: dict[str, str, str, str, str] = {  # Style for powershell
    "background": "#012456",
    "insertbackground": "#eeedf0",
    "selectbackground": "#fedba9",
    "selectforeground": "#11120f",
    "foreground": "#cccccc",
}

COMMAND: dict[str, str, str, str, str] = {  # Style for normal "cmd.exe"
    "background": "#000000",
    "insertbackground": "#f2f2f2",
    "selectbackground": "#f3f3f3",
    "selectforeground": "#000000",
    "foreground": "#f2f2f2",
}

GIT: dict[str, str, str, str, str] = {
    "background": "#000000",
    "insertbackground": "#bfbfbf",
    "selectbackground": "#bfbfbf",
    "selectforeground": "#0E0E0E",
    "foreground": "#efefef",
}

# User custom style
CUSTOM: dict[str, str, str, str, str] = load_style()
