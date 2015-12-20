import matplotlib.pyplot as plt
from scipy.fftpack import rfft

'''
From main it called

from scipy.io import wavfile
from function import *
import numpy as np

filename = 'chaikovsky30.wav'
fs, data = wavfile.read(filename) # load the data
signal = data.T[0] # this is a two channel soundtrack, I get the first track
time = np.arange(len(data))/float(fs)

ampl_freq(signal, time)
ampl(signal, time)
spectrum(signal)
'''


def ampl_freq(signal, time):
    normal_signal = [(ele / 2 ** 16.) * 2 - 1 for ele in signal]  # this is 8-bit track, b is now normalized on [-1,1)
    fft_result = rfft(normal_signal)  # calculate real part fourier transform (complex numbers list)
    len(fft_result)
    d = int(len(fft_result)/22050)
    print(d)
    nr = []
    for i in range(0, len(fft_result)):
        if i % d == 0:
            nr.append(fft_result[i])
    print("AAA")
    print(nr)
    plt.plot(nr, 'r')
    plt.show()
    plt.savefig('apl_freq.png')
    #plt.clf()


def spectrum(signal):
    plt.specgram(
        signal,
        Fs=44100,
        noverlap=int(128 * 0.5))
    plt.savefig('spectrum.png')
    plt.clf()


def ampl(signal, time):
    a = len(signal)
    b = len(time)
    plt.plot(time[:(b - 1)], signal[:(a - 1)])
    plt.savefig('amplitude.png')
    plt.clf()
