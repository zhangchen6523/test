# from tkinter import *
#
# root = Tk()
# root.title("label-test")
# root.geometry("1200x500")
# root.resizable(width=True, height=False)
# l = Label(root, text="label", bg="pink", font=("Arial", 12), width=8, height=3)
# l.pack(side=LEFT)
# root.mainloop()
# import sys
# print(sys.path)
import numpy as np
a = np.array([[2,3,4],[5,6,7]],dtype=np.int)
print(a.sum(axis=1))
print(a.shape)
#
# A = np.random.randint(0,10,size=(3,4,5,6))
#
#
# testa = np.arange(4)
# print(help(np.arange))
# print(testa)
#
# b = testa.copy()
# testa[0] = 10
# print(testa)
# print(b)

# def test(text):
#     print(text)
#
# test(aaa="aaa")