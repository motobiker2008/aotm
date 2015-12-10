import matplotlib.pyplot as plt
from scipy.fftpack import rfft


def apl_freq(a, filename):
    b = [(ele / 2 ** 8.) * 2 - 1 for ele in a]  # this is 8-bit track, b is now normalized on [-1,1)
    c = rfft(b)  # calculate real part fourier transform (complex numbers list)
    d = len(c)
    plt.plot(abs(c[:(d - 1)]), 'r')
    plt.savefig(filename+'apl_freq.png')
    plt.clf()


def spectrum_freq(a, filename):
    Pxx, freqs, t, plot = plt.specgram(
        a,
        Fs=44100,
        noverlap=int(128 * 0.5))
    plt.savefig(filename+'spectrum.png')
    plt.clf()