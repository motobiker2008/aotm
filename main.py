# coding: utf-8
from kivy.core.audio import Sound
from player import play
from plotting import plot
from reader import read_wav

__author__ = 'vladimir'

import Tkinter as tk
from Tkinter import *
from tkFileDialog import *

class Application(tk.Frame):
    def __init__(self, master=None, width=100, height=100):
        tk.Frame.__init__(self, master)
        self.createWidgets()
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.pack()

    def createWidgets(self):

        self.sound_process = None
        self.v = tk.StringVar()
        self.entry = tk.Entry(None, textvariable=self.v)
        self.entry.pack(side="left")
        s = self.v.get()

        self.open = tk.Button(self)
        self.open["text"] = "Brows"
        self.open["command"] = self.askopenfile
        self.open.pack(side="right")

    def on_closing(self):
        self.sound_process.kill()
        root.destroy()

    def askopenfile(self):
        fname = askopenfilename()
        self.v.set(fname)
        samplerate, samples = read_wav(fname)
        sp = play(fname)
        self.sound_process = sp
        plot(samples)

root = tk.Tk()
app = Application(master=root)
app.mainloop()