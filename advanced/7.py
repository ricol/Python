#!/usr/bin/env python
#-*- coding: utf-8 -*-

class TestSlots(object):
    __slots__ = ["name", "age"]
    def __init__(self, name, age):
        self.name = name
        self.age = age

ts = TestSlots("a", 1)
ts.name = 1
print(ts.name)