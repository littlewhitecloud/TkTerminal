"""An example for style"""
from tktermwidget import POWERSHELL, Config

styleconfig = Config(usetheme=True, basedon=POWERSHELL)
# if usetheme enable, the window will use sv_ttk theme
# basedon mean you can create your style based on the "basedon" style
styleconfig.mainloop()
