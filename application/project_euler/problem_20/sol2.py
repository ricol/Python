#!/usr/bin/env python
#-*- coding: utf-8 -*-

from math import factorial
def main():
    print(sum([int(x) for x in str(factorial(100))]))
if __name__ == '__main__':
    main()