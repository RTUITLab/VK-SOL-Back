import time
import os
import binascii

class Secret():

    sec = ""
    time_ = 5
    symbols = 8
    def __init__(self, _time=5, _symbols=8):
        global time_, symbols, sec
        time_ = _time
        symbols = _symbols
        sec = binascii.hexlify(os.urandom(symbols)).decode('UTF-8')
    def update(self):
        global time_, symbols, sec
        while(True):
            time.sleep(time_)
            sec = binascii.hexlify(os.urandom(symbols)).decode('UTF-8')
    def getSec(self):
        global sec
        return sec