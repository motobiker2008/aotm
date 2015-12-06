# coding: utf-8
from kivy.core.audio import Sound
from scipy.fftpack import fft
from scipy.io import wavfile
from WavHeader import get_wave_header
from player import play
from plotting import plot, plot_on_fly
from reader import read_wav
import numpy as np

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
        self.process_it(fname)

    def process_it(self, fname):
        header = get_wave_header(fname)
        bits_per_sample = header['BitsPerSample']
        channels = header['NumChannels']
        samplerate, samples = wavfile.read(fname) # load the data
        if channels == 2:
            samples = samples.T[0]
        times = np.arange(len(samples))/float(samplerate)
        s=[(ele/2**bits_per_sample)*2-1 for ele in samples] # now normalized on [-1,1)
        sp = play(fname)
        self.sound_process = sp
        print(samples[:10])
        #plot_on_fly(samples, times)
        fourie_samples = fft(s) # calculate fourier transform (complex numbers list)
        plot(fourie_samples[:len(fourie_samples)/2-1])

root = tk.Tk()
app = Application(master=root)
app.mainloop()