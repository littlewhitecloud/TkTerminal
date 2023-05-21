from __future__ import annotations

from os import getcwd
from platform import system
from subprocess import PIPE, Popen
from tkinter import Event, Misc, Text
from tkinter.ttk import Frame

SYSTEM = system()
if SYSTEM == "Windows":
    from subprocess import CREATE_NEW_CONSOLE


class Terminal(Frame):
    """A terminal widget for tkinter applications"""

    command_inserts: dict[str, str] = {
        "Windows": "PS {command}>",
        "Linux": "{command}$",
        "Darwin": "{command}$",
    }

    def __init__(self, master: Misc) -> None:
        Frame.__init__(self, master)

        # Create text widget
        self.text = Text(
            self,
            background="#2B2B2B",
            insertbackground="#DCDCDC",
            selectbackground="#b4b3b3",
            relief="flat",
            foreground="#cccccc",
            font=("Georgia", 12),
        )
        self.text.pack(expand=True, fill="both")

        # Create command prompt
        self.text.insert(
            "insert",
            f"{Terminal.command_inserts[SYSTEM].format(command=getcwd())} ",
        )

        # Set variables
        self.index = 1
        self.current_process: Popen | None = None

        # Bind events
        self.text.bind("<Key>", self.keypress)
        self.text.bind("<Return>", self.loop, add=True)

    def loop(self, _: Event) -> str:
        """Create an input loop"""
        cmd = self.text.get(f"{self.index}.0", "end-1c")
        # Determine command based on system
        cmd = cmd.split("$")[-1]  # Unix
        if SYSTEM == "Windows":
            cmd = cmd.split(">")[-1]

        # If the command is "clear" or "cls", clear the screen
        if cmd in ["clear", "cls"]:
            self.text.delete("1.0", "end")
            self.text.insert(
                "insert",
                f"{Terminal.command_inserts[SYSTEM].format(command=getcwd())} ",
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
            f"{Terminal.command_inserts[SYSTEM].format(command=getcwd())} ",
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
                    f"{Terminal.command_inserts[SYSTEM].format(command=getcwd())} ",
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
