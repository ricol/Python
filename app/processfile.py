#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

if len(os.sys.argv) <= 1:
    print("usage: processfile.py <file>")
    exit()
file = os.sys.argv[1]
with open(file, 'r') as f:
    content = f.read()
    size = len(content)
    i = 0
    while i < size:
        char = content[i]
        print "%c" % char
        i += 1
print("\n")
