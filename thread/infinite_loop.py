#!/usr/bin/env python
#-*- coding: utf-8 -*-

import multiprocessing
import threading

def loop():
    x = 0
    while True:
        x ^= 1

for i in range(multiprocessing.cpu_count()):
    t = threading.Thread(target=loop)
    t.start()

print("end")