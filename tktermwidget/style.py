"""Styles for terminal widget"""
from __future__ import annotations

from json import dump, load
from pathlib import Path
from tkinter import Text, Tk
from tkinter.colorchooser import askcolor
from tkinter.ttk import Button, Entry, Frame, Label

from platformdirs import user_cache_dir

# Constants
STYLE_PATH = Path(user_cache_dir("tktermwidget"))
JSON_FILE = STYLE_PATH / "styles.json"

# Styles format:
# {yourstylename}: dict[str] = {
#    "background": "{yourhexcolor}",
#    "insertbackground": "{yourhexcolor}",
#    "selectbackground": "{yourhexcolor}",
#    "selectforeground": "{yourhexcolor}",
#    "foreground": "{yourhexcolor}",
# }

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


# Functions
def write_style(**styles) -> None:
    """Write the style into the json file"""
    # User can call this function to write the style without gui
    # TODO: improve it, new style will overwrite the old
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        dump(styles, f, indent=1)


def load_style() -> dict:
    """Load the style from the json file"""
    # Also, user can call this function to get the style
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return load(f)


# Class
class Config(Tk):
    """ "A config gui for user to edit their custom styles"""

    def __init__(self, usetheme: bool = False):
        super().__init__()
        if usetheme:
            from darkdetect import isDark
            from sv_ttk import set_theme

            set_theme("dark" if isDark() else "light")
            self.option_add("*font", ("Cascadia Mono", 9, "normal"))

        self.geometry("855x525")
        self.title("Config your custom style")
        self.resizable(False, False)

        self.style: dict[str] = DEFAULT if load_style() == "{}" else load_style()

        # Widgets
        create = Label(self, text="Create your custom style")
        backgroundframe = Frame(self)
        background = Label(backgroundframe, text="Choose or input your normalbackground hex color")
        backgroundentry = Entry(backgroundframe)
        backgroundbutton = Button(
            backgroundframe, text="...", width=3, command=lambda: self.selectcolor(backgroundentry, "background")
        )

        insertbackgroundframe = Frame(self)
        insertbackground = Label(insertbackgroundframe, text="Choose or input your insertbackground hex color")
        insertbackgroundentry = Entry(insertbackgroundframe)
        insertbackgroundbutton = Button(
            insertbackgroundframe,
            text="...",
            width=3,
            command=lambda: self.selectcolor(insertbackgroundentry, "insertbackground"),
        )

        selectbackgroundframe = Frame(self)
        selectbackground = Label(selectbackgroundframe, text="Choose or input your selectbackground hex color")
        selectbackgroundentry = Entry(selectbackgroundframe)
        selectbackgroundbutton = Button(
            selectbackgroundframe,
            text="...",
            width=3,
            command=lambda: self.selectcolor(selectbackgroundentry, "selectbackground"),
        )

        selectforegroundframe = Frame(self)
        selectforeground = Label(selectforegroundframe, text="Choose or input your selectforeground hex color")
        selectforegroundentry = Entry(selectforegroundframe)
        selectforegroundbutton = Button(
            selectforegroundframe,
            text="...",
            width=3,
            command=lambda: self.selectcolor(selectforegroundentry, "selectforeground"),
        )

        foregroundframe = Frame(self)
        foreground = Label(foregroundframe, text="Choose or input your selectforeground hex color")
        foregroundentry = Entry(foregroundframe)
        foregroundbutton = Button(
            foregroundframe, text="...", width=3, command=lambda: self.selectcolor(foregroundentry, "foreground")
        )

        buttonframe = Frame(self)
        save = Button(buttonframe, text="Save", width=5, command=self.savestyle)
        cancel = Button(buttonframe, text="Cancel", width=5, command=self.destroy)

        self.render = Text(
            self,
            width=40,
            background=self.style["background"],
            insertbackground=self.style["insertbackground"],
            selectbackground=self.style["selectbackground"],
            selectforeground=self.style["selectforeground"],
            foreground=self.style["foreground"],
            font=("Cascadia Mono", 9, "normal"),
            relief="flat",
        )

        self.render.insert("insert", "This is a normal text for test style.")
        self.render.tag_add("select", "1.31", "1.36")
        self.render.tag_config(
            "select", background=self.style["selectbackground"], foreground=self.style["selectforeground"]
        )
        self.render["state"] = "disable"

        if usetheme:
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

        self.render.pack(side="right", fill="y", padx=3, pady=3)
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

        for widget in (
            backgroundframe,
            insertbackgroundframe,
            selectbackgroundframe,
            selectforegroundframe,
            foregroundframe,
        ):
            widget.pack(side="top", fill="y")

    def selectcolor(self, entry: Entry, name: str) -> None:
        """Select the color in the gui and insert it into the
        entry, also update the render with the lastest style"""
        color = askcolor()[-1]  # get the hex color
        entry.delete(0, "end")
        entry.insert("insert", color)
        self.style[name] = color  # store the hex color and the color name
        self.updaterender()  # update the render to show the latest style

    def updaterender(self) -> None:
        """Let the render show with the latest style"""
        self.render.config(
            background=self.style["background"],
            insertbackground=self.style["insertbackground"],
            selectbackground=self.style["selectbackground"],
            selectforeground=self.style["selectforeground"],
            foreground=self.style["foreground"],
        )
        self.render.tag_config(
            "select", background=self.style["selectbackground"], foreground=self.style["selectforeground"]
        )
        self.update()

    def savestyle(self) -> None:
        """Save the style"""
        write_style(
            background=self.style["background"],
            insertbackground=self.style["insertbackground"],
            selectbackground=self.style["selectbackground"],
            selectforeground=self.style["selectforeground"],
            foreground=self.style["foreground"],
        )
        self.destroy()


if __name__ == "__main__":
    configstyle = Config(True)
    configstyle.mainloop()
