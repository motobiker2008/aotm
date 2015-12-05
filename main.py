# coding: utf-8
from kivy.core.audio import Sound
from player import play

__author__ = 'vladimir'

import tkinter as tk
from tkinter import filedialog

class Application(tk.Frame):
    def __init__(self, master=None, width=100, height=100):
        tk.Frame.__init__(self, master)
        self.createWidgets()
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
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
    def on_closing(self):
        print("Closing")
        self.soun_process.kill()
        root.destroy()

    def askopenfile(self):
        fname = filedialog.askopenfilename()
        self.v.set(fname)
        print(fname)
        sp = play(fname)
        self.soun_process = sp

root = tk.Tk()
app = Application(master=root)
app.mainloop()