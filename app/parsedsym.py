#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

# traverse root directory, and list directories as dirs and files as files
def getListOfFiles(dir, filetype):
    result = []
    for root, dirs, files in os.walk(dir):
        path = root.split(os.sep)
        p = '/'.join(path)
        for file in files:
            f = "%s/%s" % (p, file)
            if filetype.lower() in f.lower():
                result.append(f)
    return result

def process(dir, data):
    pass

if __name__ == "__main__":
    dir = "./"
    if len(os.sys.argv) <= 1:
        print("Usage: parsedsym.py <dir>")
        exit()
    else:
        dir = os.sys.argv[1]
    filetype = "dSYM"
    print("searching for %s files in %s" % (filetype, dir))
    files = getListOfFiles(dir, filetype)
    total = len(files)
    for f in files:
        print(f)
    print("Result:")
    print("Total[%s]: %d" % (filetype, total))
