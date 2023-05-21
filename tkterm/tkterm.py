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
            f"{Terminal.command_inserts[SYSTEM].format(command=getcwd())} ",
        )
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

        process = Popen(
            cmd,
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
            stdin=PIPE,
            text=True,
            creationflags=CREATE_NEW_CONSOLE if SYSTEM == "Windows" else 0,
            cwd=getcwd(),  # Until a solution for changing the working directory is found, this will have to do
        )
        # Check if the command was successful
        returncode = process.wait()
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
