"""Styles for terminal widget"""
from __future__ import annotations

from json import dump, load
from pathlib import Path
from re import match
from tkinter import Event, Frame, Text, Tk
from tkinter.colorchooser import askcolor
from tkinter.ttk import Button, Entry, Label

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

    def __init__(self, usetheme: bool = False, basedon: dict[str] = DEFAULT):
        super().__init__()
        self.geometry("855x525")
        self.title("Config your custom style")
        self.resizable(False, False)
        self.iconbitmap("")  # Must call this function or we can't get the hwnd

        if usetheme:
            from darkdetect import isDark
            from sv_ttk import set_theme

            set_theme("dark" if isDark() else "light")
            self.option_add("*font", ("Cascadia Mono", 9))

            if isDark():
                from ctypes import byref, c_int, sizeof, windll

                windll.dwmapi.DwmSetWindowAttribute(
                    windll.user32.GetParent(self.winfo_id()), 20, byref(c_int(2)), sizeof(c_int(2))
                )
                self.withdraw()
                self.deiconify()

        self.style: dict[str] = basedon if basedon != DEFAULT else load_style() if load_style() != {} else DEFAULT

        # Color choose or input widgets
        # TODO: check the hex color is it vaild
        buttonframe = Frame(self)
        save = Button(buttonframe, text="Save", width=6, command=self.savestyle)
        cancel = Button(buttonframe, text="Cancel", width=6, command=self.destroy)

        create = Label(self, text="✨ Create your custom style ✨")
        backgroundframe = Frame(self)
        background = Label(backgroundframe, text="Choose or input your normalbackground hex color")
        backgroundentry = Entry(backgroundframe)
        backgroundbutton = Button(backgroundframe, command=lambda: self.selectcolor(backgroundentry, "background"))

        insertbackgroundframe = Frame(self)
        insertbackground = Label(insertbackgroundframe, text="Choose or input your insertbackground hex color")
        insertbackgroundentry = Entry(insertbackgroundframe)
        insertbackgroundbutton = Button(
            insertbackgroundframe,
            command=lambda: self.selectcolor(insertbackgroundentry, "insertbackground"),
        )

        selectbackgroundframe = Frame(self)
        selectbackground = Label(selectbackgroundframe, text="Choose or input your selectbackground hex color")
        selectbackgroundentry = Entry(selectbackgroundframe)
        selectbackgroundbutton = Button(
            selectbackgroundframe,
            command=lambda: self.selectcolor(selectbackgroundentry, "selectbackground"),
        )

        selectforegroundframe = Frame(self)
        selectforeground = Label(selectforegroundframe, text="Choose or input your selectforeground hex color")
        selectforegroundentry = Entry(selectforegroundframe)
        selectforegroundbutton = Button(
            selectforegroundframe,
            command=lambda: self.selectcolor(selectforegroundentry, "selectforeground"),
        )

        foregroundframe = Frame(self)
        foreground = Label(foregroundframe, text="Choose or input your selectforeground hex color")
        foregroundentry = Entry(foregroundframe)
        foregroundbutton = Button(foregroundframe, command=lambda: self.selectcolor(foregroundentry, "foreground"))

        # Style render configs
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

        # add the theme to the button widgets if usetheme == True
        if usetheme:
            for widget in (
                backgroundbutton,
                insertbackgroundbutton,
                selectbackgroundbutton,
                selectforegroundbutton,
                foregroundbutton,
            ):
                widget.config(style="Accent.TButton", width=2, text="🎨")
            save.config(style="Accent.TButton")

        # fill the entry with hexcolor before pack
        for widget, hexcolor in zip(
            (backgroundentry, insertbackgroundentry, selectbackgroundentry, selectforegroundentry, foregroundentry),
            self.style.values(),
        ):
            widget.insert("insert", hexcolor)

        # Pack the widgets
        cancel.pack(side="right", padx=1)
        save.pack(side="right", padx=3)
        buttonframe.pack(side="bottom", fill="x")

        self.render.pack(side="right", fill="y")
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

        backgroundentry.bind("<KeyPress>", lambda event: self.checkhexcolor(event, "background"))
        insertbackgroundentry.bind("<KeyPress>", lambda event: self.checkhexcolor(event, "insertbackground"))
        selectbackgroundentry.bind("<KeyPress>", lambda event: self.checkhexcolor(event, "selectbackground"))
        selectforegroundentry.bind("<KeyPress>", lambda event: self.checkhexcolor(event, "selectforeground"))
        foregroundentry.bind("<KeyPress>", lambda event: self.checkhexcolor(event, "foreground"))

        for widget in (
            backgroundframe,
            insertbackgroundframe,
            selectbackgroundframe,
            selectforegroundframe,
            foregroundframe,
        ):
            widget.pack(side="top", fill="y", pady=3)

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

    def checkhexcolor(self, event: Event, name: str) -> None:
        """Check the hex color"""
        if match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", event.widget.get()):
            event.widget.state(["invalid"])
            self.style[name] = event.widget.get()
            self.updaterender()
        else:
            event.widget.state(["!invalid"])


CUSTOM: dict[str] = load_style()

if __name__ == "__main__":
    configstyle = Config(True, basedon=POWERSHELL)
    configstyle.mainloop()
