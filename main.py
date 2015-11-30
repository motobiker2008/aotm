# coding: utf-8
__author__ = 'vladimir'

import tkinter as tk
from tkinter import filedialog

class Application(tk.Frame):
    def __init__(self, master=None, width=100, height=100):
        tk.Frame.__init__(self, master)
        self.createWidgets()
        self.pack()

    def createWidgets(self):
        self.v = tk.StringVar()
        self.entry = tk.Entry(None, textvariable=self.v)
        self.entry.pack(side="left")
        s = self.v.get()

        self.open = tk.Button(self)
        self.open["text"] = "Brows"
        self.open["command"] = self.askopenfile
        self.open.pack(side="right")

        # self.QUIT = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        # self.QUIT.pack()

    def askopenfile(self):
        fname = filedialog.askdirectory()
        self.v.set(fname)

root = tk.Tk()
app = Application(master=root)
app.mainloop()