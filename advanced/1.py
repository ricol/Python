#!/usr/bin/env python
#-*- coding: utf-8 -*-

class TestNew(object):
    def __new__(cls, * args, ** kwargs):
        print('__new__ called.')
        return super(TestNew, cls).__new__(cls, *args,  ** kwargs)
    def __init__(self):
        print('__init__ called.')
        self.a = 1

tn = TestNew()
print(tn.a)
