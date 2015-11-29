# coding: utf-8
import pprint
import wave

__author__ = 'vladimir'

def get_wav_info(file):
    waveFile = wave.open(file, 'r')
    inf = waveFile.getparams()
    pprint.pprint(inf)


if __name__ == '__main__':
    #get_wav_info('a.wav')
    # pcm_data = audiotools.open("file.wav")
    # metadata = track.get_metadata()