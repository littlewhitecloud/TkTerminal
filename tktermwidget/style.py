"""Styles for terminal"""
from __future__ import annotations

from json import dump, load
from pathlib import Path

from platformdirs import user_cache_dir

# Constants
STYLE_PATH = Path(user_cache_dir("tktermwidget"))
JSON_FILE = STYLE_PATH / "styles.json"

# Built-in styles
DEFAULT: dict[str] = {  # Style for normal tkterminalwidget
    "background": "#2B2B2B",
    "insertbackground": "#DCDCDC",
    "selectbackground": "#b4b3b3",
    "selectforeground": "#e6e6e6",
    "foreground": "#cccccc",
}

POWERSHELL: dict[str] = {  # Style for powershell
    "background": "#012456",
    "insertbackground": "#eeedf0",
    "selectbackground": "#fedba9",
    "selectforeground": "#11120f",
    "foreground": "#cccccc",
}

COMMAND: dict[str] = {  # Style for normal "cmd.exe"
    "background": "#000000",
    "insertbackground": "#f2f2f2",
    "selectbackground": "#f3f3f3",
    "selectforeground": "#000000",
    "foreground": "#f2f2f2",
}

GIT: dict[str] = {  # Style for "git.exe"
    "background": "#000000",
    "insertbackground": "#bfbfbf",
    "selectbackground": "#bfbfbf",
    "selectforeground": "#0E0E0E",
    "foreground": "#efefef",
}

# Check the style file
if not STYLE_PATH.exists():
    STYLE_PATH.mkdir(parents=True)
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        dump("{}", f)

if not (JSON_FILE).exists():
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        dump("{}", f)


# Create style
def write_style(**styles) -> None:
    """Write the style into the json file"""
    # User can use this function to write with their own style
    # TODO: improve it, new style will overwrite the old style
    with open(JSON_FILE, "w", encoding="utf-8") as json_obj:
        dump(styles, json_obj, indent=1)


# Load style
def load_style() -> dict:
    """Get style from the json file"""
    # User also can use this function to get their own style
    with open(JSON_FILE, "r", encoding="utf-8") as json_obj:
        return load(json_obj)


# Config style
def config_style() -> None:
    """Config the style with the ui"""
    # TODO: improve the code
    # TODO: improve the ui
    # TODO: fix some logic bug
    from tkinter import Text, Tk
    from tkinter.colorchooser import askcolor
    from tkinter.ttk import Button, Entry, Frame, Label

    def selectcolor(entry: Entry, name: str) -> None:
        """Select the color in the ui and insert into the entry and update the render"""
        color = askcolor()[-1]
        entry.delete(0, "end")
        entry.insert("insert", color)
        style[name] = color
        renderupdate()

    def renderupdate() -> None:
        """Update the render with the latest style"""
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
        """Save the style"""
        write_style(
            background=style["background"],
            insertbackground=style["insertbackground"],
            selectbackground=style["selectbackground"],
            selectforeground=style["selectforeground"],
            foreground=style["foreground"],
        )
        config.destroy()

    # def fillentrys() -> None:

    config = Tk()
    config.geometry("855x500")
    config.title("Config your style")
    config.resizable(False, False)

    theme: bool = False
    try:
        from sv_ttk import set_theme
    except ModuleNotFoundError:
        pass
    else:
        theme = True
        set_theme("dark")
        config.option_add("*font", ("Cascadia Mono", 9))

    style: dict[str] = DEFAULT if load_style() == "{}" else load_style()

    create = Label(config, text="Create your custom style!")
    """
        for frame in (backgroundframe, insertbackgroundframe, selectbackgroundframe, selectforegroundframe, foregroundframe):
        for _list in (
            [background, "Choose or input your normalbackground hex color"], 
            [insertbackground, "Choose or input your insertbackground hex color"],
            [selectbackground, "Choose or input your selectbackground hex color"],
            [selectforeground, "Choose or input your selectforeground hex color"],
            [foreground, "Choose or input your selectforeground hex color"],
        ):
            _list[0] = Button(frame, text = _list[1])
        
        entrylist: list = []
        
        for widget in (backgroundentry, insertbackgroundentry, selectbackgroundentry, selectforegroundentry, foregroudnentry):
            widget = Entry(frame)
            entrylist.append(widget)
        
        cnt: int = 0
        for _list in (
            [backgroundbutton, "background"],
            [insertbackgroundbutton, "insertbackground"],
            [selectbackgroundbutton, "selectbackground"],
            [selectforegroundbutton, "selectforeground"],
            [foregroundbutton, "foreground"]
        ):
            _list[0] = Button(frame, text = "...", width = 3, command=lambda: selectcolor(entrylist[cnt], _list[1]))
            cnt += 1
    """
    backgroundframe = Frame(config)
    background = Label(backgroundframe, text="Choose or input your normalbackground hex color")
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

    buttonframe = Frame(config)
    save = Button(buttonframe, text="Save", command=savestyle)
    cancel = Button(buttonframe, text="Cancel", command=config.destroy)

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
        relief="flat",
    )

    render.insert("insert", "This is a normal text for test style.")
    render.tag_add("select", "1.31", "1.36")
    render.tag_config("select", background=style["selectbackground"], foreground=style["selectforeground"])
    render["state"] = "disable"

    if theme:
        for widget in (
            backgroundbutton,
            insertbackgroundbutton,
            selectbackgroundbutton,
            selectforegroundbutton,
            foregroundbutton,
            save,
        ):
            widget.config(style="Accent.TButton")

    save.pack(side="right")
    cancel.pack(side="right")
    buttonframe.pack(side="bottom", fill="x")

    render.pack(side="right", fill="y", padx=3, pady=3)
    create.pack(side="top", fill="y", pady=15)

    for widget in (
        background,
        insertbackground,
        selectbackground,
        selectforeground,
        foreground,
        backgroundentry,
        insertbackgroundentry,
        selectbackgroundentry,
        selectforegroundentry,
        foregroundentry,
        backgroundbutton,
        insertbackgroundbutton,
        selectbackgroundbutton,
        selectforegroundbutton,
        foregroundbutton,
    ):
        widget.pack(side="left", padx=3)

    for widget in (backgroundframe, insertbackgroundframe, selectbackgroundframe, selectforegroundframe, foregroundframe):
        widget.pack(side="top", fill="y")

    config.mainloop()


# Styles format:
# {yourstylename}: dict[str] = {
#    "background": "{yourhexcolor}",
#    "insertbackground": "{yourhexcolor}",
#    "selectbackground": "{yourhexcolor}",
#    "selectforeground": "{yourhexcolor}",
#    "foreground": "{yourhexcolor}",
# }

CUSTOM: dict[str] = load_style()  # User custom style

config_style()
