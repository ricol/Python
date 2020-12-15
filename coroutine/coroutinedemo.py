#!/usr/bin/env python
#-*- coding: utf-8 -*-

import multitask
import time
def coroutin_1():
    for i in range(3):
        print 'c1'
        yield i

def coroutin_2():
    for i in range(3):
        print 'c2'
        yield i

multitask.add(coroutin_1())
multitask.add(coroutin_2())
multitask.run()