#!/usr/bin/env python
#-*- coding: utf-8 -*-

#!/usr/local/bin/python3

def make_adder():
	local_val = 2
	return lambda x: x + local_val

def main():
	f = make_adder()
	print(f(10))
	print(f(2))

main()
