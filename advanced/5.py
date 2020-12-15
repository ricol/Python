#!/usr/bin/env python
#-*- coding: utf-8 -*-

class TestAttr(object):
    def __init__(self):
        self.name = "abc"

    def __getattr__(self, item):
        print("item:" + str(item))
        print("getattr")
        return 10
    def __setattr__(self, * args, ** kwargs):
        print("set attr")
        object.__setattr__(self, *args,  ** kwargs)

    def __delattr__(self, * args, ** kwargs):
        print("delete attr")
        object.__delattr__(self, *args, ** kwargs)

ta = TestAttr()
print(ta.__dict__)
print(ta.names)
del ta.name
print(ta.__dict__)