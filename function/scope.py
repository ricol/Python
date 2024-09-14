#!/usr/bin/env python
#-*- coding: utf-8 -*-

print "demo..."
x = 1

def f():
    global x
    x += 1
    print x

f()

print "demo1..."

def t(l = []):
    print "fun: l: %s" % l
    l.append('hi')
    return l

print t()
print t()

print "demo2..."

def fun(l = None):
    print "fun: l: %s" % l
    if l == None:
        l = []
    l.append("hi")
    return l

print fun()
print fun()

data = []

def test(data):
    import random
    data.append(random.randint(0, 10))

test(data)
print data
test(data)
print data

l = []

def test1():
    l.append(2)

print l 
test1()
print l

def test2():
    global l
    l += [2]

test2()
print l