"""Terminal widget for tkinter"""
from __future__ import annotations

from os import getcwd
from pathlib import Path
from platform import system
from subprocess import PIPE, Popen
from tkinter import Event, Misc, Text
from tkinter.ttk import Frame, Scrollbar

from platformdirs import user_cache_dir
from style import Default

# Set constants
HISTORY_PATH = Path(user_cache_dir("tktermwidget"))
HISTORY_FILE = HISTORY_PATH / "history.txt"
SYSTEM = system()
if SYSTEM == "Windows":
    from subprocess import CREATE_NEW_CONSOLE

    SIGN = ">"
else:
    CREATE_NEW_CONSOLE = 0
    SIGN = "$ "

# Check that the history directory exists
if not HISTORY_PATH.exists():
    HISTORY_PATH.mkdir(parents=True)
    # Also create the history file
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.close()

# Check that the history file exists
if not (HISTORY_FILE).exists():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.close()


class AutoHideScrollbar(Scrollbar):
    """Scrollbar that automatically hides when not needed"""

    def __init__(self, master=None, **kwargs):
        Scrollbar.__init__(self, master=master, **kwargs)

    def set(self, first: int, last: int):
        """Set the Scrollbar"""
        if float(first) <= 0.0 and float(last) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        Scrollbar.set(self, first, last)


class Terminal(Frame):
    """A terminal widget for tkinter applications

    Args:
        master (Misc): The parent widget
        autohide (bool, optional): Whether to autohide the scrollbars.
        (Set true to enable it.)
        *args: Arguments for the text widget
        **kwargs: Keyword arguments for the text widget

    Methods for outside use:
        None

    Methods for internal use:
        up (Event) -> str: Goes up in the history
        down (Event) -> str: Goes down in the history
        (If the user is at the bottom of the history, it clears the command)
        left (Event) -> str: Goes left in the command if the index is greater than the directory
        (So the user can't delete the directory or go left of it)
        kill (Event) -> str: Kills the current command
        loop (Event) -> str: Runs the command typed"""

    def __init__(
        self,
        master: Misc,
        style: dict = Default,
        filehistory: str = None,
        autohide: bool = False,
        *args,
        **kwargs,
    ):
        Frame.__init__(self, master)

        # Set row and column weights
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create text widget and scrollbars
        scrollbars = Scrollbar if not autohide else AutoHideScrollbar
        self.xscroll = scrollbars(self, orient="horizontal")
        self.yscroll = scrollbars(self)
        self.text = Text(
            self,
            *args,
            background=kwargs.get("background", style["background"]),
            insertbackground=kwargs.get("insertbackground", style["insertbackground"]),
            selectbackground=kwargs.get("selectbackground", style["selectbackground"]),
            selectforeground=kwargs.get("selectforeground", style["selectforeground"]),
            relief=kwargs.get("relief", "flat"),
            foreground=kwargs.get("foreground", style["foreground"]),
            xscrollcommand=self.xscroll.set,
            yscrollcommand=self.yscroll.set,
            wrap=kwargs.get("wrap", "char"),
            font=kwargs.get("font", ("Cascadia Code", 9, "normal")),
        )
        self.xscroll.config(command=self.text.xview)
        self.yscroll.config(command=self.text.yview)

        # Grid widgets
        self.text.grid(row=0, column=0, sticky="nsew")

        if kwargs.get("wrap", "char") == "none":
            self.xscroll.grid(row=1, column=0, sticky="ew")
        self.yscroll.grid(row=0, column=1, sticky="ns")

        # Create command prompt
        self.directory()

        # Set variables
        self.longflag: bool = False
        self.current_process: Popen | None = None
        self.index: int = 1
        self.cursor: int = self.text.index("insert")
        self.longsymbol: str = "\\" if not SYSTEM == "Windows" else "&&"
        self.longcmd: str = ""
        self.filehistory: str = HISTORY_FILE if not filehistory else filehistory

        self.latest: int = self.cursor

        # Bind events
        self.text.bind("<Up>", self.up, add=True)
        self.text.bind("<Down>", self.down, add=True)
        self.text.bind("<Return>", self.loop, add=True)
        for bind_str in ("<Left>", "<BackSpace>"):
            self.text.bind(bind_str, self.left, add=True)
        for bind_str in ("<Return>", "<ButtonRelease-1>"):
            self.text.bind(bind_str, self.check, add=True)
        self.text.bind("<Control-KeyPress-c>", self.kill, add=True)  # Isn't working

        # History recorder
        self.history = open(
            self.filehistory,
            "r+",
            encoding="utf-8",
        )

        self.historys = [i.strip() for i in self.history.readlines() if i.strip()]
        self.historyindex = len(self.historys) - 1

    def check(self, _: Event) -> None:
        """Update cursor"""
        self.cursor = self.text.index("insert")
        if float(self.cursor) < float(self.latest):
            self.text.bind("<KeyPress>", self.ignore, True)
            self.text.bind("<KeyPress-BackSpace>", self.ignore, True)
        elif float(self.cursor) >= float(self.latest):
            self.text.unbind("<Key>")
            self.text.unbind("<KeyPress-Backspace>")

    def directory(self) -> None:
        """Insert the directory"""
        self.text.insert("insert", getcwd() + SIGN)

    def newline(self) -> None:
        """Insert a newline"""
        self.text.insert("insert", "\n")
        self.index += 1

    def ignore(self, _: Event) -> str:
        """Ignore the event"""
        return "break"

    def up(self, _: Event) -> str:
        """Go up in the history"""
        if self.historyindex >= 0:
            self.text.delete(f"{self.index}.0", "end-1c")
            self.directory()
            # Insert the command
            self.text.insert("insert", self.historys[self.historyindex].strip())
            self.historyindex -= 1
        return "break"

    def down(self, _: Event) -> str:
        """Go down in the history"""
        if self.historyindex < len(self.historys) - 1:
            self.text.delete(f"{self.index}.0", "end-1c")
            self.directory()
            # Insert the command
            self.text.insert("insert", self.historys[self.historyindex].strip())
            self.historyindex += 1
        else:
            # Clear the command
            self.text.delete(f"{self.index}.0", "end-1c")
            self.directory()
        return "break"

    def left(self, _: Event) -> str:
        """Go left in the command if the command is greater than the path"""
        insert_index = self.text.index("insert")
        dir_index = f"{insert_index.split('.')[0]}.{len(getcwd() + SIGN)}"
        if insert_index == dir_index:
            return "break"

    def kill(self, _: Event) -> str:
        """Kill the current process"""
        if self.current_process:
            self.current_process.kill()
            self.current_process = None
        return "break"

    def update(self) -> str:
        """Update or the command has no output"""
        self.directory()
        self.check(None)
        self.latest = self.text.index("insert")
        self.text.see("end")
        return "break"

    def loop(self, _: Event) -> str:
        """Create an input loop"""
        # Get the command from the text
        cmd = self.text.get(f"{self.index}.0", "end-1c")
        cmd = cmd.split(SIGN)[-1].strip()

        if self.longflag:
            self.longcmd += cmd
            cmd = self.longcmd
            self.longcmd = ""
            self.longflag = False

        if cmd.endswith(self.longsymbol):
            self.longcmd += cmd.split(self.longsymbol)[0]
            self.longflag = True
            self.newline()
            return "break"

        if cmd:  # Record the command if it isn't empty
            self.history.write(cmd + "\n")
            self.historys.append(cmd)
            self.historyindex = len(self.historys) - 1
        else:  # Leave the loop
            self.newline()
            self.directory()
            self.text.see("end")
            return "break"

        # Check the command if it is a special command
        if cmd in ["clear", "cls"]:
            self.text.delete("1.0", "end")
            self.directory()
            return "break"
        elif cmd == "exit":
            self.master.quit()

        # Check that the insert position is at the end
        if self.text.index("insert") != f"{self.index}.end":
            self.text.mark_set("insert", f"{self.index}.end")
            self.text.see("insert")

        # TODO: Refactor the way we get output from subprocess
        # Run the command
        self.current_process = Popen(
            cmd,
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
            stdin=PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            cwd=getcwd(),  # TODO: use dynamtic path instead (see #35)
            creationflags=CREATE_NEW_CONSOLE,
        )
        # The following needs to be put in an after so the kill command works

        # Check if the command was successful
        output: tuple = self.current_process.communicate()
        returnlines: str = output[0]
        errors: str = output[1]
        returncode = self.current_process.returncode
        self.current_process = None
        if returncode != 0:
            returnlines += errors  # If the command was unsuccessful, it doesn't give stdout
        # TODO: Get the success message from the command (see #16)
        # Output to the text
        self.newline()
        for line in returnlines:
            self.text.insert("insert", line)
            if line == "\n":
                self.index += 1

        # Update the text and the index
        self.update()
        return "break"  # Prevent the default newline character insertion


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

    # Set the minimum size
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
