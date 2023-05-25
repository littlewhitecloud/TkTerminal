from __future__ import annotations

from os import getcwd
from platform import system
from subprocess import PIPE, Popen
from tkinter import Event, Misc, Text
from tkinter.ttk import Frame, Scrollbar

# Set constants

SYSTEM = system()
CREATE_NEW_CONSOLE = 0
DIR = "{command}$ "
if SYSTEM == "Windows":
    from subprocess import CREATE_NEW_CONSOLE

    DIR = "PS {command}>"

class AutoHideScrollbar(Scrollbar):
    def set(self, upper, lower):
        if float(upper) <= 0.0 and float(lower) >= 1.0:
            self.grid_remove()
        else:
            self.grid(row=0, column=1, sticky="ns")
    
        Scrollbar.set(self, upper, lower)

class Terminal(Frame):
    """A terminal widget for tkinter applications"""

    def __init__(self, master: Misc) -> None:
        Frame.__init__(self, master)

        # Set row and column weights
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create text widget and scrollbars
        self.scrollbarx = AutoHideScrollbar(self)
        self.text = Text(
            self,
            background="#2B2B2B",
            insertbackground="#DCDCDC",
            selectbackground="#b4b3b3",
            relief="flat",
            foreground="#cccccc",
            yscrollcommand=self.scrollbarx.set,
            wrap="none",
            font=("Cascadia Code", 9, "normal"),
        )
        self.scrollbarx.config(command=self.text.yview)

        # Grid widgets
        self.text.grid(row=0, column=0, sticky="nsew")
        self.scrollbarx.grid(row=0, column=1, sticky="ns")

        # Create command prompt
        self.text.insert(
            "insert",
            f"{DIR.format(command=getcwd())}",
        )

        # Set variables
        self.index = 1
        self.current_process: Popen | None = None

        # Bind events
        self.text.bind("<Key>", self.keypress, add=True)
        self.text.bind("<Return>", self.loop, add=True)
        
        # History recorder
        self.history = open("history.txt", "r+")
        self.historys = self.history.read().split("\n")
        self.hi = len(self.historys) # hi: History Index
        
    def loop(self, _: Event) -> str:
        """Create an input loop"""
        cmd = self.text.get(f"{self.index}.0", "end-1c")
        # Determine command based on system
        cmd = cmd.split("$")[-1]  # Unix
        if SYSTEM == "Windows":
            cmd = cmd.split(">")[-1].strip()
        
        # Record the command
        self.history.write(cmd)
        
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

    def keypress(self, event: Event) -> str:
        """Handle keypresses"""

        # Control + c cancels the current process
        if event.state == 4 and event.keysym == "c":
            if self.current_process is not None:
                self.current_process.kill()
                self.current_process = None
                self.text.insert(
                    "insert",
                    f"{DIR.format(command=getcwd())}",
                )
                return "break"


        # TODO: Add key up and key down to show history command
        if event.keysym == "Up" or event.keysym == "Down":
            self.text.delete("%d.%d" % (self.index, len(DIR.format(command=getcwd()))), "end")
            self.text.insert(
                "insert",
                self.historys[self.hi],
            )
            if event.keysym == "Up": self.hi -= 1
            else: self.hi += 1

            return "break"         
        
if __name__ == "__main__":
    from tkinter import Tk

    from darkdetect import isDark
    from sv_ttk import set_theme

    # Create root window
    root = Tk()

    if isDark():
        set_theme("dark")
    else:
        set_theme("light")

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
