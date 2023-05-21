from __future__ import annotations

from os import getcwd, popen
from platform import system
from tkinter import Event, Text, Tk

SYSTEM = system()

command_inserts: dict[str, str] = {
    "Windows": "PS {command}>",
    "Linux": "{command}$",
    "Darwin": "{command}$",
}


class Terminal(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.withdraw()

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
        self.index = 1

        self.text.insert("insert", command_inserts[SYSTEM].format(command=getcwd()))
        self.text.bind("<KeyPress-Return>", self.loop)
        self.resize()
        self.deiconify()

    def resize(self) -> None:
        """Detect the minimum size of the app, get the center of the screen, and place the app there."""
        # Update widgets so minimum size is accurate
        self.update_idletasks()

        # Get minimum size
        minimum_width: int = self.winfo_reqwidth()
        minimum_height: int = self.winfo_reqheight()

        # Get center of screen based on minimum size
        x_coords = int(self.winfo_screenwidth() / 2 - minimum_width / 2)
        y_coords = int(self.wm_maxsize()[1] / 2 - minimum_height / 2)

        # Place app and make the minimum size the actual minimum size (non-infringable)
        self.geometry(f"{minimum_width}x{minimum_height}+{x_coords}+{y_coords}")
        self.wm_minsize(minimum_width, minimum_height)

    def loop(self, _: Event) -> str:
        """Create an input loop"""
        cmd = self.text.get(f"{self.index}.0", "end-1c")
        # Determine command based on system
        cmd = cmd.split("$")[-1]  # Unix
        if SYSTEM == "Windows":
            cmd = cmd.split(">")[-1]

        # If the command is clear or cls, clear the screen
        if cmd in ["clear", "cls"]:
            self.text.delete("1.0", "end")
            self.text.insert("insert", command_inserts[SYSTEM].format(command=getcwd()))
            return "break"

        returnlines = popen(cmd)
        returnlines = returnlines.readlines()

        self.text.insert("insert", "\n")
        self.index += 1
        for line in returnlines:
            self.text.insert("insert", line)
            self.index += 1

        # Remove the next two lines that cause the extra newlines
        self.text.insert("insert", command_inserts[SYSTEM].format(command=getcwd()))
        return "break"  # Prevent the default newline character insertion


example = Terminal()
example.mainloop()
