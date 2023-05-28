from __future__ import annotations

from os import getcwd
from pathlib import Path
from platform import system
from subprocess import PIPE, Popen
from tkinter import Event, Misc, Text
from tkinter.ttk import Frame, Scrollbar

from platformdirs import user_cache_dir

# Set constants

HISTORY_PATH = Path(user_cache_dir("tkterm"))
SYSTEM = system()
CREATE_NEW_CONSOLE = 0
DIR = "{command}$ "
if SYSTEM == "Windows":
    from subprocess import CREATE_NEW_CONSOLE

    DIR = "PS {command}>"

# Check that the history directory exists
if not HISTORY_PATH.exists():
    HISTORY_PATH.mkdir(parents=True)
    # Also create the history file
    open(HISTORY_PATH / "history.txt", "w").close()

# Check that the history file exists
if not (HISTORY_PATH / "history.txt").exists():
    open(HISTORY_PATH / "history.txt", "w").close()

class AutoHideScrollbar(Scrollbar):
    """Scrollbar that automatically hides when not needed"""
    def __init__(self, master=None, **kwargs):
        Scrollbar.__init__(self, master=master, **kwargs)

    def set(self, l, h):
        if float(l) <= 0.0 and float(h) >= 1.0:
            self.grid_remove()
        else:
            self.grid()

        Scrollbar.set(self, l, h)

class Terminal(Frame):
    """A terminal widget for tkinter applications"""

    def __init__(self, master: Misc) -> None:
        Frame.__init__(self, master)

        # Set row and column weights
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create text widget and scrollbars
        self.xscroll = AutoHideScrollbar(self, orient="horizontal")
        self.yscroll = AutoHideScrollbar(self)
        self.text = Text(
            self,
            background="#2B2B2B",
            insertbackground="#DCDCDC",
            selectbackground="#b4b3b3",
            relief="flat",
            foreground="#cccccc",
            xscrollcommand=self.xscroll.set,
            yscrollcommand=self.yscroll.set,
            wrap="none",
            font=("Cascadia Code", 9, "normal"),
        )
        self.xscroll.config(command=self.text.xview)
        self.yscroll.config(command=self.text.yview)

        # Grid widgets
        self.text.grid(row=0, column=0, sticky="nsew")
        self.xscroll.grid(row=1, column=0, sticky="ew")
        self.yscroll.grid(row=0, column=1, sticky="ns")

        # Create command prompt
        self.text.insert(
            "insert",
            f"{DIR.format(command=getcwd())}",
        )

        # Set variables
        self.index = 1
        self.current_process: Popen | None = None

        # Bind events
        self.text.bind("<Up>", self.up, add=True)
        self.text.bind("<Down>", self.down, add=True)
        self.text.bind("<Return>", self.loop, add=True)

        # History recorder
        self.history = open(HISTORY_PATH / "history.txt", "r+")
        self.historys = self.history.readlines()
        print(self.historys)
        self.hi = len(self.historys) - 1

    def loop(self, _: Event) -> str:
        """Create an input loop"""
        cmd = self.text.get(f"{self.index}.0", "end-1c")
        # Determine command based on system
        cmd = cmd.split("$")[-1]  # Unix
        if SYSTEM == "Windows":
            cmd = cmd.split(">")[-1].strip()

        # Record the command
        if cmd != "":
            self.history.write(cmd + "\n")
            self.historys.append(cmd)
            self.hi = len(self.historys) - 1

        # If the command is "clear" or "cls", clear the screen
        if cmd in ["clear", "cls"]:
            self.text.delete("1.0", "end")
            self.text.insert(
                "insert",
                f"{DIR.format(command=getcwd())}",
            )
            return "break"

        self.current_process = Popen(
            cmd,
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
            stdin=PIPE,
            text=True,
            cwd=getcwd(),  # Until a solution for changing the working directory is found, this will have to do
            creationflags=CREATE_NEW_CONSOLE,
        )
        # Check if the command was successful
        returncode = self.current_process.wait()
        process = self.current_process
        self.current_process = None
        returnlines = process.stdout.readlines()
        if returncode != 0:
            returnlines += (
                process.stderr.readlines()
            )  # If the command was unsuccessful, it doesn't give stdout
            # TODO: Get the success message from the command (see #16)

        self.text.insert("insert", "\n")
        self.index += 1
        for line in returnlines:
            self.text.insert("insert", line)
            self.index += 1

        self.text.insert(
            "insert",
            f"{DIR.format(command=getcwd())}",
        )
        return "break"  # Prevent the default newline character insertion

    def up(self, _: Event) -> str:
        """Go up in the history"""
        if self.hi >= 0:
            self.text.delete(f"{self.index}.0", "end-1c")
            # Insert the directory
            self.text.insert(
                "insert",
                f"{DIR.format(command=getcwd())}",
            )
            # Insert the command
            self.text.insert("insert", self.historys[self.hi].strip())
            self.hi -= 1
        return "break"

    def down(self, _: Event) -> str:
        """Go down in the history"""
        if self.hi < len(self.historys) - 1:
            self.text.delete(f"{self.index}.0", "end-1c")
            # Insert the directory
            self.text.insert(
                "insert",
                f"{DIR.format(command=getcwd())}",
            )
            # Insert the command
            self.text.insert("insert", self.historys[self.hi].strip())
            self.hi += 1
        else:
            # Clear the command
            self.text.delete(f"{self.index}.0", "end-1c")
            # Insert the directory
            self.text.insert(
                "insert",
                f"{DIR.format(command=getcwd())}",
            )
        return "break"


if __name__ == "__main__":
    from tkinter import Tk

    # Create root window
    root = Tk()

    # Hide root window during initialization
    root.withdraw()

    # Set title
    root.title("Terminal")

    # Create terminal
    term = Terminal(root)
    term.pack(expand=True, fill="both")

    # Set minimum size and center app

    # Update widgets so minimum size is accurate
    root.update_idletasks()

    # Get minimum size
    minimum_width: int = root.winfo_reqwidth()
    minimum_height: int = root.winfo_reqheight()

    # Get center of screen based on minimum size
    x_coords = int(root.winfo_screenwidth() / 2 - minimum_width / 2)
    y_coords = int(root.wm_maxsize()[1] / 2 - minimum_height / 2)
    # Place app and make the minimum size the actual minimum size (non-infringable)
    root.geometry(f"{minimum_width}x{minimum_height}+{x_coords}+{y_coords}")
    root.wm_minsize(minimum_width, minimum_height)

    # Show root window
    root.deiconify()

    # Start mainloop
    root.mainloop()
