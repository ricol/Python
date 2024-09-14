#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

def read_file(fpath):
    BLOCK_SIZE = 1024
    with open(fpath, 'rb') as f:
        while True:
            block = f.read(BLOCK_SIZE)
            if block:
                yield block
            else:
                return

print(os.sys.argv)
if len(os.sys.argv) <= 1:
    print("Usage: read_file.py <filename>")
else:
    filename = os.sys.argv[1]
    content = read_file(filename)
    while True:
        try:
            b = content.next()
            print(b)
        except StopIteration as s:
            print("end.")
