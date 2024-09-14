#!/usr/bin/env python3
#-*- coding: utf-8 -*-

def f():
	yield "f..."

def g():
	yield from f()

for i in g():
	print(i)
