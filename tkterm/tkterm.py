from __future__ import annotations

from os import getcwd, popen
from platform import system
from tkinter import Event, Misc, Text
from tkinter.ttk import Frame


class Terminal(Frame):
    SYSTEM = system()

    command_inserts: dict[str, str] = {
        "Windows": "PS {command}>",
        "Linux": "{command}$",
        "Darwin": "{command}$",
    }

    def __init__(self, master: Misc) -> None:
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

        returnlines = popen(
            cmd
        )  # Does not show errors, also runs in the terminal running the script
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


if __name__ == "__main__":
    from tkinter import Tk

    root = Tk()
    root.title("Terminal")
    term = Terminal(root)
    term.pack(expand=True, fill="both")
    root.mainloop()
