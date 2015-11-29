# coding: utf-8
__author__ = 'vladimir'
import subprocess


def wav_to_mp3(in_file, out_file, rate=44100, channels=2, bits=192):
    bashCommand = "ffmpeg -y -i {in_file} -vn -ar {rate} -ac {channels} -ab {bits} -f mp3 {out_file}".format(
        in_file=in_file, rate=rate, channels=channels, bits=bits, out_file=out_file)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]


def mp3_to_wav(in_file, out_file):
    bashCommand = "ffmpeg -y -i {in_file} {out_file}".format(in_file=in_file, out_file=out_file)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]


if __name__ == '__main__':
    wav_to_mp3('a.wav', 'a.mp3')
    mp3_to_wav('a1.mp3', 'a1.wav')