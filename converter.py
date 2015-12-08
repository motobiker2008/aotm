# coding: utf-8
__author__ = 'vladimir'
import subprocess


def wav_to_mp3(in_file, out_file, rate=44100, channels=2, bits=192):
    bashCommand = "ffmpeg -y -i {in_file} -vn -ar {rate} -ac {channels} -ab {bits} -f mp3 {out_file}".format(
        in_file=in_file, rate=rate, channels=channels, bits=bits, out_file=out_file)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]


def mp3_to_wav(in_file, out_file, sec_in=None, sec_out=None):
    if sec_in is None or sec_out is None:
        bashCommand = "ffmpeg -y -i {in_file} {out_file}".format(in_file=in_file, out_file=out_file)
    else:
        bashCommand = "ffmpeg -y -ss {sec_in} -t {sec_out} -i {in_file} {out_file}".format(in_file=in_file, out_file=out_file,
                                                                                      sec_in=sec_in, sec_out=sec_out)
    print(bashCommand)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]


if __name__ == '__main__':
    #wav_to_mp3('a.wav', 'a.mp3')
    mp3_to_wav('ekrid.mp3', 'krid_10.wav', 0, 10)