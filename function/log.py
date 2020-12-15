#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time

def log(func):
    def wrapper(*args, ** kw):
        print('call %s():' % func.__name__)
        return func(*args, ** kw)
    return wrapper

@log
def now():
    print("Now: ", time.time())

now()

def newNow():
    print("New Now: ", time.time())

newNow()
log(newNow())
log(newNow)()
