<h1 align="center"> TkTerminal </h1>

[![PyPI](https://img.shields.io/pypi/v/tktermwidget)](https://pypi.org/project/tktermwidget)
![Platform](https://img.shields.io/powershellgallery/p/Pester?color=blue)

```TkTermianl``` 是一个使用 tkinter 用 Python 编写的终端模拟器

### Windows
<img src="images/windows.png" width="75%" align="center">

### MacOS
<img src="images/macos.png" width="85%" align="center">

## 特征
- 用户可以使用他们自己的观点来设置终端控件，就像文本控件一样
- 用 \ 来输入新行 (Windows上是&&)
- 命令历史记录
- 风格
- 等等

## 未来想法
- 语法高亮

## 风格
```tkterminalwidget``` 也有一些主题可以用 比如 ```Powershell``` ```Command```
![image](https://github.com/littlewhitecloud/TkTerminal/assets/71159641/3affd018-0408-4e91-96de-4775937e0ab8)
![image](https://github.com/littlewhitecloud/TkTerminal/assets/71159641/2b43b9d0-7569-498b-932d-e18828541d47)
但是，用这个你也可以创建自己的主题：
```python
from tktermwidget import Config, POWERSHELL

styleconfig = Config(usetheme=True, basedon=POWERSHELL)
# 如果usetheme启用的话，窗口会使用sv_ttk主题
# basedon意义是在基于“basedon”得到的主题上创建你自己的主题
styleconfig.mainloop()
```
![image](https://github.com/littlewhitecloud/TkTerminal/assets/71159641/09a53045-8806-4e63-9045-741bcce65e99)

在保存完它之后，你可以写下下面的代码来创建你自己的主题:

```python
from tkinterwidget import Terminal, CUSTOM
example = Terminal(window, style=CUSTOM) #你自己的主题
example.mainloop()
```
或者使用一个构建好的主题
```python
from tkinterwidget import Terminal, POWERSHELL # 用Powershell举例
example = Terminal(window, style=POWERSHELL)
example.mainloop()
```

## 安装:
```console
pip install tktermwidget
```

## 样例:
```python
# -*- coding: gbk -*-
from tkinter import Tk

from tkterm import Terminal

# 创建窗口
root = Tk()

# 隐藏窗口
root.withdraw()

# 设置标题
root.title("Terminal")

# 创建终端
term = Terminal(root)
term.pack(expand=True, fill="both")

# 设置窗口大小以及位置

# 更新，使部件准确无误
root.update_idletasks()

# 获取窗口最小值
minimum_width: int = root.winfo_reqwidth()
minimum_height: int = root.winfo_reqheight()

# 获取屏幕中间值
x_coords = int(root.winfo_screenwidth() / 2 - minimum_width / 2)
y_coords = int(root.wm_maxsize()[1] / 2 - minimum_height / 2)

# 放置应用程序并将最小大小设置为实际最小大小
root.geometry(f"{minimum_width}x{minimum_height}+{x_coords}+{y_coords}")
root.wm_minsize(minimum_width, minimum_height)

# 显示窗口
root.deiconify()

# 开始循环
root.mainloop()
```


