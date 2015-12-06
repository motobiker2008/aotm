# coding: utf-8
import time
from reader import read_wav

__author__ = 'vladimir'

import numpy as np
from matplotlib import pyplot as plt


def plot(samples):
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    plt.title("Sample Wav")
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