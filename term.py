from CustomTkinterTitlebar import CTT
from tkinter import Text, BOTH, FLAT, INSERT

class Terminal(CTT):
	def __init__(self, ):
		super().__init__()
		self.titlebarconfig(color = {"color": "#2B2B2B", "color_nf": "#2f2f2f"}, height = 40)
		self.usetitle(False)
		self.useicon(False)
		self.geometry("1000x515")

		self.update()
		self.text = Text(self, background = "#2B2B2B" , insertbackground = "#DCDCDC", selectbackground = "#b4b3b3", relief = FLAT, foreground = "#cccccc")
		self.text.configure(font = ("Cascadia Code", 10, "normal")) # Link to settings later
		self.text.pack(expand = True, fill = BOTH)
		
	def Displayer(self, msg):
		""" Display a returned message from console """
		self.text.insert(INSERT, msg)

example = Terminal()
example.mainloop()
