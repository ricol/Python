#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

def readfile(filename):
    result = []
    with open(filename, 'r') as f:
        for line in f:
            result += [int(x.strip()) for x in line.rstrip(", \n").split(",")]
    return result

def main():
    if len(os.sys.argv) <= 1:
        print("usage: count <filename>")
        exit()
    lst = readfile(os.sys.argv[1])
    print(lst)

if __name__ == "__main__":
    main()