<h1 align="center"> TkTerminal </h1>

[![PyPI](https://img.shields.io/pypi/v/tktermwidget)](https://pypi.org/project/tktermwidget)
![Platform](https://img.shields.io/powershellgallery/p/Pester?color=blue)

### 🌏 [简体中文](README_CH.md)

```TkTerminal``` is a terminal emulator written in Python using tkinter. It is quite easy to use.
### Windows
<img src="images/windows.png" width="75%" align="center">

### MacOS
<img src="images/macos.png" width="85%" align="center">

## Features
- User can set the terminal widget with their own options
- Use \ to make new lines (On Windows it is &&)
- Command history recorder
- Styles
- And some on

## Future ideas
- Highlight

## Styles
```tkterminalwidget``` also have some styles to use such as ```Powershell``` ```Command```:
![image](https://github.com/littlewhitecloud/TkTerminal/assets/71159641/3affd018-0408-4e91-96de-4775937e0ab8)
![image](https://github.com/littlewhitecloud/TkTerminal/assets/71159641/2b43b9d0-7569-498b-932d-e18828541d47)
But also, you can create your custom style by using
```python
from tktermwidget import Config, POWERSHELL

styleconfig = Config(usetheme=True, basedon=POWERSHELL)
# if usetheme enable, the window will use sv_ttk theme
# basedon mean you can create your style based on the "basedon" style
styleconfig.mainloop()
```
![image](https://github.com/littlewhitecloud/TkTerminal/assets/71159641/09a53045-8806-4e63-9045-741bcce65e99)

After saving it, you can write down this to use the custom theme:
```python
from tkinterwidget import Terminal, CUSTOM
example = Terminal(window, style=CUSTOM) # your custom theme
example.mainloop()
```
Or use a built in theme:
```python
from tkinterwidget import Terminal, POWERSHELL # use powershell for an example
example = Terminal(window, style=POWERSHELL)
example.mainloop()
```

## Installation:
```console
pip install tktermwidget
```

## Example:
```python
from tkinter import Tk

from tkterm import Terminal

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
```
