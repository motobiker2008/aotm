# coding: utf-8
__author__ = 'vladimir'
import scipy.io.wavfile as wa
def read_wav(fname):
    samplerate, samples = wav.read(fname)
    return samplerate, samples