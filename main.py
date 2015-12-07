# coding: utf-8
from kivy.core.audio import Sound
from multiprocessing.pool import ThreadPool
from scipy.fftpack import fft
from scipy.io import wavfile
import threading
from time import sleep
from WavHeader import get_wave_header
from player import play
from plotting import plot, plot_on_fly, plot_amplitude_online, plot_spectrum
from reader import read_wav
import numpy as np

__author__ = 'vladimir'

import Tkinter as tk
from Tkinter import *
from tkFileDialog import *

def worker(bits_per_sample, samples):
    s=[(ele/2**bits_per_sample)*2-1 for ele in samples]
    return fft(s)

def fft_thread(bits_per_sample, samples):
    pool = ThreadPool(processes=1)
    async_result = pool.run(worker, (bits_per_sample, samples))
    return async_result

def plot_wave_thread(fourie_samples):
    pool = ThreadPool(processes=1)
    async_result = pool.apply_async(plot_spectrum, (fourie_samples, ))
    async_result.get()

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
        bits_per_sample = float(header['BitsPerSample'])/1
        channels = header['NumChannels']
        samplerate, samples = wavfile.read(fname)
        if channels == 2:
            samples = samples.T[0]
        times = np.arange(len(samples))/float(samplerate)
        time = len(samples)/float(samplerate)
        step = int(len(times)/(time*4)) #0.985

        #async_result = fft_thread(bits_per_sample, samples)

        fourie_samples = worker(bits_per_sample, samples)
        sp = play(fname)
        self.sound_process = sp
        plot_amplitude_online(samples, times, step) #async_result.get()
        #plot_wave_thread(fourie_samples)
        plot_spectrum(fourie_samples)
        # plot(fourie_samples[:len(fourie_samples)/2-1], samplerate)

root = tk.Tk()
app = Application(master=root)
app.mainloop()