# coding: utf-8
import pprint
import wave

__author__ = 'vladimir'

def get_wav_info(file):
    waveFile = wave.open(file, 'r')
    inf = waveFile.getparams()
    pprint.pprint(inf)


if __name__ == '__main__':
    pass
    get_wav_info('chaikovsky.wav')
    # pcm_data = audiotools.open("file.wav")
    # metadata = track.get_metadata()