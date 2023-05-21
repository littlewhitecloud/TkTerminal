from os import getcwd, popen
from tkinter import Event, Text, Tk


class Terminal(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.update()
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

        self.text.insert("insert", f"PS {getcwd()}>")
        self.text.bind("<KeyPress-Return>", self.loop)

    def resize(self, _: Event):
        """Detect the minimum size of the app, get the center of the screen, and place the app there."""
        # Update widgets so minimum size is accurate
        self.update_idletasks()

        # Get minimum size
        minimum_width: int = self.winfo_reqwidth()
        minimum_height: int = self.winfo_reqheight()

        # Get center of screen based on minimum size
        x_coords = int(self.winfo_screenwidth() / 2 - minimum_width / 2)
        y_coords = int(self.winfo_screenheight() / 2 - minimum_height / 2) - 20
        # `-20` should deal with Dock on macOS and looks good on other OS's

        # Place app and make the minimum size the actual minimum size (non-infringable)
        self.geometry(f"{minimum_width}x{minimum_height}+{x_coords}+{y_coords}")
        self.wm_minsize(minimum_width, minimum_height)

    def loop(self, _: Event):
        """Create an input loop"""
        cmd = self.text.get(f"{self.index}.0", "end-1c")
        cmd = cmd.split(">")[-1]

        returnlines = popen(cmd)
        returnlines = returnlines.readlines()

        self.text.insert("insert", "\n")
        self.index += 1
        for line in returnlines:
            self.text.insert("insert", line)
            self.index += 1

        # Remove the next two lines that cause the extra newlines
        self.text.insert("insert", f"PS {getcwd()}>")
        return "break"  # Prevent the default newline character insertion


example = Terminal()
example.mainloop()
