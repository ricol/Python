#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys

filename = sys.argv[1]

print("reading...", filename)

with open(filename, 'rb') as f:
    data = f.read(10)
    print("size: ", len(data))
    print("content: ", data)

print("done.")
