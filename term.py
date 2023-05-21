from CustomTkinterTitlebar import CTT
from tkinter import Text, BOTH, FLAT, INSERT
from os import popen, getcwd

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
		self.useblur()
		self.index = 1.0

		self.Displayer("PS %s>" % getcwd())
		self.text.bind("<KeyPress-Return>", self.Loop)
		
	def Displayer(self, msg):
		""" Display a returned message from console """
		self.text.insert(INSERT, msg)

	def Loop(self, event):
		""" Create a input loop """
		cmd = self.text.get(self.index, "end-1c")
		cmd = cmd.split(">")[-1]
		
		returnline = popen(cmd)
		returnline = returnline.readlines()
		
		self.Displayer('\n')
		self.index += 1.0
		for l in returnline:
			self.Displayer(l)
			self.index += 1.0
		
		self.Displayer("PS %s>" % getcwd()) # There is a bug...

example = Terminal()
example.mainloop()

