from tkinter import *

fontSize = 12
root = Tk()
root.title("测试程序")
root.geometry("1200x500")
root.resizable(width=False, height=False)
l = Label(root, text="测试开始", bg="black", font=("Arial", fontSize), width=8, height=3)
l.pack(side=TOP)
b = Button(root, text="点击处理", font=("Arial", fontSize), width=8, height=3)
b.pack(side=LEFT)
root.mainloop()