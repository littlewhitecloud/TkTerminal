from tkinter import Tk

from tktermwidget import Terminal

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
