"""An exmaple for style"""
from tktermwidget import POWERSHELL, Config

styleconfig = Config(usetheme=True, basedon=POWERSHELL)
# 如果usetheme启用的话，窗口会使用sv_ttk主题
# basedon意义是在基于“basedon”得到的主题上创建你自己的主题
styleconfig.mainloop()
