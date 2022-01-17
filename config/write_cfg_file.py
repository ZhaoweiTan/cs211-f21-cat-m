#!/usr/bin/env python3

import serial
import sys

class SBuf:
    def __init__(self, sout):
        self.b = bytearray()
        self.s = sout

    def feed(self, d):
        t = []

        for i in range(0,len(d)):
            t.append(d[i])
            if d[i] == 0x7E:
                self.b += bytes(t)
                self.s.write(self.b)
                self.b = bytes()
                t = []
                print('Out')

        if len(t) > 0:
            self.b += bytes(t)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Error: Usage ./collect.py PORT BAUDRATE INPUT.')
        sys.exit(-1)

    serial_out = serial.Serial(sys.argv[1], baudrate=int(sys.argv[2]),
                               timeout=None, rtscts=True, dsrdtr=True)

    sbuf = SBuf(serial_out)

    with open(sys.argv[3], 'rb') as fin:
        d = fin.read()
        sbuf.feed(d)


