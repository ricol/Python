#!/usr/bin/env python
#-*- coding: utf-8 -*-

def addlist(alist):
    for i in alist:
        yield i + 1

alist = [1, 2, 3, 4]
for x in addlist(alist):
    print(x)

def h():
    print 'To be brave'
    yield 5
    yield 6
    yield 7

h()
c = h()
for i in c:
    print(i)
c = h()
print(c.next())

def h():
    print 'hello'
    m = yield 5
    print m
    d = yield 6
    print d
    print 'end h.'

c = h()
c.next()
c.send('ricol')
c.next()
c.send('wang')

def test():
    print("begin...")
    for x in range(10):
        yield x
    print("end.")

d = test()
for i in d:
    print(i)