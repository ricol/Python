#!/usr/bin/env python
#-*- coding: utf-8 -*-

import math
from io import StringIO

def isSorted(data):
    for i in range(1, len(data)):
        if data[i - 1] > data[i]: return False
    return True

def isHeap(data, index):
    l = index * 2 + 1
    r = l + 1
    if l < len(data):
        if data[index] < data[l]: return False
        if not isHeap(data, l): return False
    if r < len(data):
        if data[index] < data[r]: return False
        if not isHeap(data, r): return False
    return True

def show_tree(tree, total_width=60, fill=' '):
    """Pretty-print a tree.
    total_width depends on your input size"""
    output = StringIO()
    last_row = -1
    for i, n in enumerate(tree):
        if i:
            row = int(math.floor(math.log(i+1, 2)))
        else:
            row = 0
        if row != last_row:
            output.write(u'\n')
        columns = 2**row
        col_width = int(math.floor((total_width * 1.0) / columns))
        output.write(u'%s' % (str(n).center(col_width, fill)))
        last_row = row
    print ('-' * total_width)
    print (output.getvalue())
    print ('-' * total_width)
    return