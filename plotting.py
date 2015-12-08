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
    plt.show()
    x=[]
    y=[]
    for i in range(0, len(data)-1, step):
        x.append(times[i])
        y.append(data[i])
        plt.clf()
        plt.xlabel('time (s)')
        plt.ylabel('amplitude')
        plt.plot(x,y)
        plt.pause(0.000000001)

def plot_spectrum(data):

    plt.xlabel('frequencies')
    plt.ylabel('amplitude')
    plt.plot(abs(data), 'r')
    plt.show()


def logscale_spec(spec, sr=44100, factor=20.):
    timebins, freqbins = np.shape(spec)

    scale = np.linspace(0, 1, freqbins) ** factor
    scale *= (freqbins-1)/max(scale)
    scale = np.unique(np.round(scale))

    # create spectrogram with new freq bins
    newspec = np.complex128(np.zeros([timebins, len(scale)]))
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            newspec[:,i] = np.sum(spec[:,scale[i]:], axis=1)
        else:
            newspec[:,i] = np.sum(spec[:,scale[i]:scale[i+1]], axis=1)

    # list center freq of bins
    allfreqs = np.abs(np.fft.fftfreq(freqbins*2, 1./sr)[:freqbins+1])
    freqs = []
    for i in range(0, len(scale)):
        if i == len(scale)-1:
            freqs += [np.mean(allfreqs[scale[i]:])]
        else:
            freqs += [np.mean(allfreqs[scale[i]:scale[i+1]])]

    return newspec, freqs


def plot(samplerate, samples, fourie_samples):
    s = fourie_samples
    binsize=2**10
    colormap="jet"
    sshow, freq = logscale_spec(s, factor=1.0, sr=samplerate)
    ims = 20.*np.log10(np.abs(sshow)/10e-6) # amplitude to decibel

    timebins, freqbins = np.shape(ims)

    plt.figure(figsize=(15, 7.5))
    plt.imshow(np.transpose(ims), origin="lower", aspect="auto", cmap=colormap, interpolation="none")
    plt.colorbar()

    plt.xlabel("time (s)")
    plt.ylabel("frequency (hz)")
    plt.xlim([0, timebins-1])
    plt.ylim([0, freqbins])

    xlocs = np.float32(np.linspace(0, timebins-1, 5))
    plt.xticks(xlocs, ["%.02f" % l for l in ((xlocs*len(samples)/timebins)+(0.5*binsize))/samplerate])
    ylocs = np.int16(np.round(np.linspace(0, freqbins-1, 10)))
    plt.yticks(ylocs, ["%.02f" % freq[i] for i in ylocs])



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