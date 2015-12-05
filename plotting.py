# coding: utf-8
import time
from reader import read_wav

__author__ = 'vladimir'

import numpy as np
from matplotlib import pyplot as plt

def plot(samples):
    #plt.axis([0, 1000, 0, 1])
    #plt.ion()
    #fig=plt.figure() # make a figure
    #plt.show()
    xList=[]
    yList=[]
    try:
        for i in range(1, len(samples)):
            plt.scatter(i, samples[i][1])
            plt.draw()
            plt.pause(0.0001)
    except Exception:
        plt.close('all')

if __name__ == '__main__':
    samplerate, samples = read_wav("chaikovsky.wav")
    print(samples[2000:44000])
    #plot(samples)