#!/usr/bin/env python
#-*- coding: utf-8 -*-

def consumer():
    r = 'Consumer start...'
    num = 1
    while True:
        n = yield r
        if not n:
            print('quit' + str(n))
            return
        print('[CONSUMER] Consuming ' + str(n) + '...')
        r = str(num) + ' OK'
        num += 1

def consumer1():
    r = 'Consumer1 start...'
    yield 1
    yield 2
    yield 3

def produce(c):
    print('Producer start...')
    r = c.send(None)
    print(r)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing ' + str(n) + '...')
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    print(c.close())

def test(c):
    for i in c:
        print(i)
    pass

def test1(c):
    print(c.next())
    print(c.next())
    print(c.next())

c = consumer1()
# produce(c)
# test(c)
test1(c)