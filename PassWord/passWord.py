import tkinter as tk
import hashlib
import base64


# 定义MainUI类表示应用/窗口，继承Frame类
class MainUI(tk.Frame):
    # Application构造函数，master为窗口的父控件
    def __init__(self, master=None):
        # 初始化Application的Frame部分
        tk.Frame.__init__(self, master)
        # 显示窗口，并使用grid布局
        self.grid()
        # 创建控件
        self.createTextFiled()

    def createTextFiled(self):
        self.passLabel = tk.Label(self,text="加密密码")
        self.oldPassLabel = tk.Label(self, text="原密码")
        # 创建一个标签，输出要显示的内容
        self.passWordText = tk.Entry(self,width=50)
        self.oldPassWordText = tk.Entry(self,width=50)

        self.passLabel.grid(row=0,column=0)
        self.oldPassLabel.grid(row=1, column=0)
        # 设定使用grid布局
        self.passWordText.grid(row=0, column=1)
        self.oldPassWordText.grid(row=1, column=1)

        # 创建一个按钮，用来触发answer方法
        self.clickButton = tk.Button(self, text="解密原密码", command=(self.answer))
        # 设定使用grid布局
        self.clickButton.grid(row=2,column=1)

    def answer(self):
        # 创建md5对象
        # hl = hashlib.md5()
        # hl.update(self.passWordText.get().encode(encoding='utf-8'))
        # self.oldPassWordText.insert(0, hl.hexdigest())
        jiemi(self.passWordText.get())
        self.oldPassWordText.insert(0,jiemi(self.passWordText.get()))
        # jiami('aaaaaaa')
        # self.oldPassWordText.insert(0,self.passWordText.get().encode(encoding='utf-8'))


def jiami(str):
    name = str
    name = name.encode('utf-8')
    a = base64.b64encode(name)
    print(a)
    # base64解密

def jiemi(str):
    b = base64.b64decode(str)
    c = b.decode('utf-8')
    return c

# 创建一个MainUI对象
app = MainUI()
# 设置窗口标题
app.master.title('获取密码小工具')
# 设置窗体大小
app.master.geometry('410x100')
# 主循环开始
app.mainloop()