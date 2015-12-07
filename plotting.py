# coding: utf-8
import matplotlib.animation as animation
import time
from reader import read_wav

__author__ = 'vladimir'

import numpy as np
from matplotlib import pyplot as plt

def plot_amplitude_online(data, times, step):
    #times = len(data)
    plt.ion()
    plt.xlim(times[0], times[-1])
    plt.xlabel('time (s)')
    plt.ylabel('amplitude')
    plt.show()
    x=[]
    y=[]
    for i in range(0, len(data)-1, step):
        x.append(times[i])
        y.append(data[i])
        plt.clf()
        plt.plot(x,y)
        plt.pause(0.000000001)

def plot(samples, samplerate):
    time= len(samples)/float(samplerate)
    plt.colorbar()
    plt.xlabel("time (s)")
    plt.ylabel("frequency")
    plt.xlim([0, time-1])
    plt.ylim([0, 44100])

    # plt.ylabel("Amplitude")
    # plt.xlabel("Time")
    # plt.title("Sample Wav")
    #axes = plt.gca()
    print(time, samplerate)
    #axes.set_xlim([0,time])
    #axes.set_ylim([0,samplerate])
    print(samples[:20])
    plt.plot(abs(samples), 'r')
    plt.show()


def plot_on_fly(samples, times):
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    plt.title("Sample Wav")
    try:
        for i in range(1, len(samples)):
            plt.scatter(samples[i], times[i], marker='o')
            plt.draw()
            plt.pause(0.000001)
    except Exception as e:
        print(e)
        plt.close('all')




if __name__ == '__main__':
    samplerate, samples = read_wav("chaikovsky.wav")
    times = np.arange(len(samples))/float(samplerate)
    print(len(samples), samplerate)
    print(samples[:])
    plot(samples, times)