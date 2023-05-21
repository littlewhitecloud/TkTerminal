from __future__ import annotations

from os import getcwd, popen
from platform import system
from tkinter import Event, Frame, Text, Tk

root = Tk()
root.title("Terminal")
root.withdraw()


class Terminal(Frame):
    SYSTEM = system()

    command_inserts: dict[str, str] = {
        "Windows": "PS {command}>",
        "Linux": "{command}$",
        "Darwin": "{command}$",
    }

    def __init__(self, master: Tk) -> None:
        Frame.__init__(self, master)

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

        self.text.insert(
            "insert",
            f"{Terminal.command_inserts[Terminal.SYSTEM].format(command=getcwd())} ",
        )
        self.text.bind("<Return>", self.loop, add=True)

    def loop(self, _: Event) -> str:
        """Create an input loop"""
        cmd = self.text.get(f"{self.index}.0", "end-1c")
        # Determine command based on system
        cmd = cmd.split("$")[-1]  # Unix
        if Terminal.SYSTEM == "Windows":
            cmd = cmd.split(">")[-1]

        # If the command is clear or cls, clear the screen
        if cmd in ["clear", "cls"]:
            self.text.delete("1.0", "end")
            self.text.insert(
                "insert",
                f"{Terminal.command_inserts[Terminal.SYSTEM].format(command=getcwd())} ",
            )
            return "break"

        returnlines = popen(cmd)
        returnlines = returnlines.readlines()

        self.text.insert("insert", "\n")
        self.index += 1
        for line in returnlines:
            self.text.insert("insert", line)
            self.index += 1

        self.text.insert(
            "insert",
            f"{Terminal.command_inserts[Terminal.SYSTEM].format(command=getcwd())} ",
        )
        return "break"  # Prevent the default newline character insertion


def resize(master: Tk) -> None:
    """Detect the minimum size of the app, get the center of the screen, and place the app there."""
    # Update widgets so minimum size is accurate
    master.update_idletasks()

    # Get minimum size
    minimum_width: int = master.winfo_reqwidth()
    minimum_height: int = master.winfo_reqheight()

    # Get center of screen based on minimum size
    x_coords = int(master.winfo_screenwidth() / 2 - minimum_width / 2)
    y_coords = int(master.wm_maxsize()[1] / 2 - minimum_height / 2)

    # Place app and make the minimum size the actual minimum size (non-infringable)
    master.geometry(f"{minimum_width}x{minimum_height}+{x_coords}+{y_coords}")
    master.wm_minsize(minimum_width, minimum_height)


terminal = Terminal(root)
terminal.pack(expand=True, fill="both")

resize(root)
root.deiconify()
root.mainloop()
