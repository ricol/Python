#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import string

def process_file(filename):
    hist = dict()
    with open(filename) as fp:
        for line in fp:
            process_line(line, hist)
    return hist

def process_line(line, hist):
    line = line.replace('-', ' ')

    for word in line.split():
        word = word.strip(string.punctuation + string.whitespace)
        word = word.lower()
        hist[word] = hist.get(word, 0) + 1

def total_words(hist):
    return sum(hist.values())

def different_words(hist):
    return len(hist)

def most_common(hist):
    t = []
    for key, value in hist.items():
        t.append((value, key))
    t.sort(reverse=True)
    return t

if len(os.sys.argv) <= 1:
    print("Usage: count.py <filename>")
else:
    hist = process_file(os.sys.argv[1])
    print("Total number of words: %d" % total_words(hist))
    print("Number of different words: %d" % different_words(hist))
    t = most_common(hist)
    print("The most common workds are:")
    for f, w in t[0:10]:
        print("%d\t%s" % (f, w))