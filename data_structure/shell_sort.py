#!/usr/bin/env python
#-*- coding: utf-8 -*-

import funs
import random

def shellSort(array, n):

    # Rearrange elements at each n/2, n/4, n/8, ... intervals
    for gap in range(10, -1, -1):
        for i in range(gap, n):
            temp = array[i]
            j = i
            while j >= gap and array[j - gap] > temp:
                array[j] = array[j - gap]
                j -= gap

            array[j] = temp

LEN = int(1e4)
print 'generating...'
data = [random.randint(0, LEN) for _ in range(LEN)]
print 'sorting...'
shellSort(data, len(data))
print 'complete.'
print 'checking...' + str(funs.isSorted(data))