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

    def set(self, length, height):
        if float(length) <= 0.0 and float(height) >= 1.0:
            self.grid_remove()
        else:
            self.grid()

        Scrollbar.set(self, length, height)


class Terminal(Frame):
    """A terminal widget for tkinter applications

    Args:
        master (Misc): The parent widget
        autohide (bool, optional): Whether to autohide the scrollbars. Defaults to True.
        *args: Arguments for the text widget
        **kwargs: Keyword arguments for the text widget

    Methods for outside use:
        None

    Methods for internal use:
        up (Event) -> str: Goes up in the history
        down (Event) -> str: Goes down in the history (if the user is at the bottom of the history, it clears the command)
        left (Event) -> str: Goes left in the command if the index is greater than the length of the directory (so the user can't delete the directory or go left of it)
        kill (Event) -> str: Kills the current command
        loop (Event) -> str: Runs the command typed"""

    def __init__(self, master: Misc, autohide: bool = True, *args, **kwargs):
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
            background=kwargs.get("background", "#2B2B2B"),
            insertbackground=kwargs.get("insertbackground", "#DCDCDC"),
            selectbackground=kwargs.get("selectbackground", "#b4b3b3"),
            relief=kwargs.get("relief", "flat"),
            foreground=kwargs.get("foreground", "#cccccc"),
            xscrollcommand=self.xscroll.set,
            yscrollcommand=self.yscroll.set,
            wrap=kwargs.get("wrap", "char"),
            font=kwargs.get("font", ("Cascadia Code", 9, "normal")),
        )
        self.xscroll.config(command=self.text.xview)
        self.yscroll.config(command=self.text.yview)

        # Grid widgets
        self.text.grid(row=0, column=0, sticky="nsew")
        self.xscroll.grid(row=1, column=0, sticky="ew")
        self.yscroll.grid(row=0, column=1, sticky="ns")

        # Create command prompt
        self.directory()

        # Set variables
        self.index = 1
        self.current_process: Popen | None = None
        
        # Bind events & tags
        self.text.bind("<Up>", self.up, add=True)
        self.text.bind("<Down>", self.down, add=True)
        self.text.bind("<Left>", self.left, add=True)
        self.text.bind("<Return>", self.loop, add=True)
        self.text.bind("<BackSpace>", self.left, add=True)
        self.text.mark_set("io", "end-1c")
        
        # TODO: Refactor the way we get output from subprocess
        self.text.bind("<Control-KeyPress-c>", self.kill, add=True) # Isn't working

        # History recorder
        self.history = open(HISTORY_PATH / "history.txt", "r+")
        self.historys = [i.strip() for i in self.history.readlines() if i.strip()]
        self.hi = len(self.historys) - 1
    
    def directory(self):
        """Insert the directory"""
        self.text.insert(
            "insert",
            f"{DIR.format(command=getcwd())}",
        )

    def up(self, _: Event) -> str:
        """Go up in the history"""
        if self.hi >= 0:
            self.text.delete(f"{self.index}.0", "end-1c")
            # Insert the directory
            self.directory()
            # Insert the command
            self.text.insert("insert", self.historys[self.hi].strip())
            self.hi -= 1
        return "break"

    def down(self, _: Event) -> str:
        """Go down in the history"""
        if self.hi < len(self.historys) - 1:
            self.text.delete(f"{self.index}.0", "end-1c")
            # Insert the directory
            self.directory()
            # Insert the command
            self.text.insert("insert", self.historys[self.hi].strip())
            self.hi += 1
        else:
            # Clear the command
            self.text.delete(f"{self.index}.0", "end-1c")
            # Insert the directory
            self.directory()
        return "break"

    def left(self, _: Event) -> str:
        """Go left in the command if the command is greater than the path"""
        insert_index = self.text.index("insert")
        dir_index = f"{insert_index.split('.')[0]}.{len(DIR.format(command=getcwd()))}"
        if insert_index == dir_index:
            return "break"

    def kill(self, _: Event) -> str:
        """Kill the current process"""
        if self.current_process:
            self.current_process.kill()
            self.current_process = None
        return "break"

    def loop(self, _: Event) -> str:
        """Create an input loop"""
        cmd = self.text.get(f"{self.index}.0", "end-1c")
        # Determine command based on system
        if SYSTEM == "Windows":
            cmd = cmd.split(">")[-1].strip()
        else:
            cmd = cmd.split("$")[-1].strip()  # Unix

        # Record the command
        if cmd != "":
            self.history.write(cmd + "\n")
            self.historys.append(cmd)
            self.hi = len(self.historys) - 1
        else:
            self.text.insert("insert", "\n")
            self.index += 1
            self.directory()
            return "break"

        # Check that the insert position is at the end
        if self.text.index("insert") != f"{self.index}.end":
            self.text.mark_set("insert", f"{self.index}.end")
            self.text.see("insert")

        # If the command is "clear" or "cls", clear the screen
        if cmd in ["clear", "cls"]:
            self.text.delete("1.0", "end")
            self.directory()
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
        )  # The following needs to be put in an after so the kill command works and the program doesn't freeze
        # Check if the command was successful
        returnlines, errors, = self.current_process.communicate()
        process = self.current_process
        returncode = self.current_process.returncode
        self.current_process = None
        if returncode != 0:
            returnlines += errors # If the command was unsuccessful, it doesn't give stdout
            # TODO: Get the success message from the command (see #16)

        self.text.insert("insert", "\n")
        self.index += 1
        for line in returnlines:
            self.text.insert("insert", line)
            if line == "\n":
                self.index += 1

        self.directory()
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
