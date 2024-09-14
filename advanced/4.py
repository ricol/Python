#!/usr/bin/env python
#-*- coding: utf-8 -*-

class TestCall(object):
    def __call__(self):
        print("call it")
tc = TestCall()
tc()