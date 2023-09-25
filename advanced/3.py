#!/usr/bin/env python
#-*- coding: utf-8 -*-

class TestIterNext(object):
    def __init__(self, data=1):
        self.data = data

    def next(self):
        if self.data > 5:
            raise StopIteration
        else:
            self.data += 1
            return self.data

    def __iter__(self):
        return self

for t in TestIterNext(): print(t)
