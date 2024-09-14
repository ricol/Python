#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
import os

# traverse root directory, and list directories as dirs and files as files
def getListOfJsons(dir):
    jsons = []
    for root, dirs, files in os.walk(dir):
        path = root.split(os.sep)
        p = '/'.join(path)
        for file in files:
            f = "%s/%s" % (p, file)
            filename, fileextension = os.path.splitext(f)
            if fileextension == '.json':
                jsons.append(f)
    return jsons

def json_validator(data):
    try:
        json.loads(data)
        return True
    except ValueError as error:
        return False

if __name__ == "__main__":
    search_dir = "./"
    if len(os.sys.argv) <= 1:
        print("Usage: validatejson.py <directory>")
        exit()
    else:
        search_dir = os.sys.argv[1]
    print("searching for json files in %s" % search_dir)
    print("-" * 30)
    jsonDirs = getListOfJsons(search_dir)
    total = len(jsonDirs)
    ok = 0
    error = 0

    if total <= 0:
        print("No json file to validate.")
		exit()

    for dir in jsonDirs:
        with open(dir, "r") as myfile:
            data = myfile.read()
            msg = "Validating %s..." % dir.replace(search_dir, '')
            print msg,
            if json_validator(data):
                ok += 1
                print("[OK]")
            else:
                error += 1
                print("[ERROR]")
    print("-" * 30)
    print("Total: %d, OK: %d, Error: %d" % (total, ok, error))
