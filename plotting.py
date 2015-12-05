# coding: utf-8
import time
from reader import read_wav

__author__ = 'vladimir'

import numpy as np
from matplotlib import pyplot as plt

def plot(samples, times):
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    # set the title
    plt.title("Sample Wav")
    #plt.axis([0, 1000, 0, 1])
    #plt.ion()
    #fig=plt.figure() # make a figure
    #plt.show()
    # data = samples
    # plt.fill_between(times, data, color='k')
    # plt.show()
    print(len(samples), len(times))
    try:
        for i in range(1, len(samples)):
            plt.scatter(times[i], samples[i], marker=',')
            #plt.scatter(times[i], samples[i][1], markertype=',')
            plt.draw()
            plt.pause(0.0000001)
    except Exception as e:
        print(e)
        plt.close('all')

if __name__ == '__main__':
    samplerate, samples = read_wav("a1.wav")
    times = np.arange(len(samples))/float(samplerate)
    print(len(samples))
    print(samples[:])
    plot(samples, times)