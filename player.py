# coding: utf-8
import subprocess

__author__ = 'vladimir'

def play(in_file):
    process=None
    try:
        bashCommand = "play {in_file}".format(in_file=in_file)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        #output = process.communicate()[0]
        return process
    except Exception:
        process.kill()
        print("Exiting...")