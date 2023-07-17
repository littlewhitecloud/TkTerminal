"""Tkinter Terminal widget"""
from __future__ import annotations

from os import chdir, getcwd, path
from pathlib import Path
from platform import system
from subprocess import PIPE, Popen
from tkinter import Event, Misc, Text
from tkinter.ttk import Frame, Scrollbar

from platformdirs import user_cache_dir

if __name__ == "__main__":  # For develop
    from style import DEFAULT
else:
    from .style import DEFAULT

HISTORY_PATH = Path(user_cache_dir("tktermwidget"))
HISTORY_FILE = HISTORY_PATH / "history.txt"
SYSTEM = system()
CREATE_NEWCONSOLE = 0
SIGN = "$ "

if SYSTEM == "Windows":  # Check if platform is windows
    from subprocess import CREATE_NEW_CONSOLE

    SIGN = ">"


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
        style (dict, optional): Set the style for the Terminal widget
        filehistory (str, optional): Set your own file history instead of the normal
        autohide (bool, optional): Whether to autohide the scrollbars. Set true to enable.
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
        check (Event) -> None: Update cursor and check it if is out of the edit range
        execute (Event) -> str: Execute the command"""

    def __init__(
        self, master: Misc, style: dict = DEFAULT, filehistory: str = None, autohide: bool = False, *args, **kwargs
    ):
        Frame.__init__(self, master)

        # Set row and column weights
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create text widget and x, y scrollbar
        self.style: dict = style
        horizontal: bool = False
        scrollbar = Scrollbar if not autohide else AutoHideScrollbar

        if kwargs.get("wrap", "char") == "none":
            self.xscroll = scrollbar(self, orient="horizontal")
            horizontal = True

        self.yscroll = scrollbar(self)
        self.text = Text(
            self,
            *args,
            wrap=kwargs.get("wrap", "char"),
            yscrollcommand=self.yscroll.set,
            relief=kwargs.get("relief", "flat"),
            font=kwargs.get("font", ("Cascadia Code", 9, "normal")),
            foreground=kwargs.get("foreground", self.style["foreground"]),
            background=kwargs.get("background", self.style["background"]),
            insertbackground=kwargs.get("insertbackground", self.style["insertbackground"]),
            selectbackground=kwargs.get("selectbackground", self.style["selectbackground"]),
            selectforeground=kwargs.get("selectforeground", self.style["selectforeground"]),
        )

        if horizontal:
            self.text.config(xscrollcommand=self.xscroll.set)
            self.xscroll.config(command=self.text.xview)
        self.yscroll.config(command=self.text.yview)

        # Grid widgets
        self.text.grid(row=0, column=0, sticky="nsew")
        if horizontal:
            self.xscroll.grid(row=1, column=0, sticky="ew")
        self.yscroll.grid(row=0, column=1, sticky="ns")

        # Init command prompt
        self.directory()

        # Set constants
        self.longsymbol: str = "\\" if not SYSTEM == "Windows" else "&&"
        self.filehistory: str = HISTORY_FILE if not filehistory else filehistory

        # Set variables
        self.index: int = 1
        self.longcmd: str = ""
        self.longflag: bool = False
        self.current_process: Popen | None = None
        self.cursor: int = self.text.index("insert")

        self.latest: int = self.cursor

        # History recorder
        self.history = open(
            self.filehistory,
            "r+",  # Both read and write
            encoding="utf-8",
        )

        self.historys = [i.strip() for i in self.history.readlines()]
        self.historyindex = len(self.historys) - 1

        # Bind events
        self.text.bind("<Up>", self.up, add=True)
        self.text.bind("<Down>", self.down, add=True)
        self.text.bind("<Return>", self.execute, add=True)
        for bind_str in ("<Left>", "<BackSpace>"):
            self.text.bind(bind_str, self.left, add=True)
        for bind_str in ("<Return>", "<ButtonRelease-1>", "<Left>", "<Right>"):
            self.text.bind(bind_str, self.check, add=True)

        self.text.bind("<Control-KeyPress-c>", self.kill, add=True)  # Isn't working

        del horizontal

    def check(self, _: Event) -> None:
        """Update cursor and check if it is out of the edit range"""
        self.cursor = self.text.index("insert")  # Update cursor
        if float(self.cursor) < float(self.latest):
            for bind_str in ("<KeyPress>", "<KeyPress-BackSpace>"):
                self.text.bind(bind_str, lambda _: "break", add=True)
        else:
            for unbind_str in ("<KeyPress>", "<KeyPress-BackSpace>"):
                self.text.unbind(unbind_str)

    def directory(self) -> None:
        """Insert the directory"""
        self.text.insert("insert", getcwd() + SIGN)

    def kill(self, _: Event) -> str:
        """Kill the current process"""
        if self.current_process:
            self.current_process.terminate()
            self.current_process = None
        return "break"

    def execute(self, _: Event) -> str:
        """Execute the command"""
        # Get the line from the text
        cmd: str = self.text.get(f"{self.index}.0", "end-1c")
        # Split the command from the line also strip
        cmd = cmd.split(SIGN)[-1].strip()

        # Special check
        if cmd.endswith(self.longsymbol):
            self.longcmd += cmd.split(self.longsymbol)[0]
            self.longflag = True
            self.newline()
            return "break"

        if self.longflag:
            cmd = self.longcmd + cmd
            self.longcmd = ""
            self.longflag = False

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
            self.index = 1
            return "break"
        elif cmd == "exit":
            self.master.quit()
        elif cmd.startswith("cd"):  # TAG: is all platform use cd...?
			# It will raise OSError instead of output a normal error
			# TODO: fix it
            if cmd == "cd..":
                chdir(path.abspath(path.join(getcwd(), "..")))
            else:
                chdir(cmd.split()[-1])
            self.newline()
            self.directory()
            return "break"

        # Set the insert position is at the end
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
            cwd=getcwd(),  # TODO: use dynamtic path instead (see #35)
            creationflags=CREATE_NEW_CONSOLE,
        )
        # The following needs to be put in an after so the kill command works

        # Check if the command was successful
        returnlines: str = ""
        errors: str = ""
        returnlines, errors = self.current_process.communicate()
        returncode = self.current_process.returncode
        self.current_process = None

        if returncode != 0:
            returnlines += errors  # If the command was unsuccessful, it doesn't give stdout
        # TODO: Get the success message from the command (see #16)

        # Output to the text
        self.newline()
        for line in returnlines:
            self.text.insert("insert", line)

        # Update the text and the index
        self.index = int(self.text.index("insert").split(".")[0])
        self.update()
        return "break"  # Prevent the default newline character insertion

    def newline(self) -> None:
        """Insert a newline"""
        self.text.insert("insert", "\n")
        self.index += 1

    def update(self) -> str:
        """Update the text widget or the command has no output"""
        # Make a newline
        self.newline()
        # Insert the directory
        self.directory()
        # Update cursor and check if it is out of the edit range
        self.check(None)
        # Update latest index
        self.latest = self.text.index("insert")
        # Warp to the end
        self.text.see("end")
        return "break"

    # Keypress
    def down(self, _: Event) -> str:
        """Go down in the history"""
        if self.historyindex < len(self.historys) - 1:
            self.text.delete(f"{self.index}.0", "end-1c")
            self.directory()
            # Insert the command
            self.text.insert("insert", self.historys[self.historyindex])
            self.historyindex += 1
        else:
            # Clear the command
            self.text.delete(f"{self.index}.0", "end-1c")
            self.directory()
        return "break"

    def left(self, _: Event) -> str | None:
        """Go left in the command if the command is greater than the path"""
        insert_index = self.text.index("insert")
        dir_index = f"{insert_index.split('.')[0]}.{len(getcwd() + SIGN)}"
        if insert_index == dir_index:
            del insert_index, dir_index
            return "break"

    def up(self, _: Event) -> str:
        """Go up in the history"""
        if self.historyindex >= 0:
            self.text.delete(f"{self.index}.0", "end-1c")
            self.directory()
            # Insert the command
            self.text.insert("insert", self.historys[self.historyindex])
            self.historyindex -= 1
        return "break"


if __name__ == "__main__":
    from tkinter import Tk

    root = Tk()
    root.withdraw()
    root.title("Terminal")

    term = Terminal(root)
    term.pack(expand=True, fill="both")

    root.update_idletasks()

    minimum_width: int = root.winfo_reqwidth()
    minimum_height: int = root.winfo_reqheight()

    x_coords = int(root.winfo_screenwidth() / 2 - minimum_width / 2)
    y_coords = int(root.wm_maxsize()[1] / 2 - minimum_height / 2)

    root.geometry(f"{minimum_width}x{minimum_height}+{x_coords}+{y_coords}")
    root.wm_minsize(minimum_width, minimum_height)

    root.deiconify()
    root.mainloop()
