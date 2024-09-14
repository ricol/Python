#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests

def cache(func):
    saved = {}

    def wrapper(url):
        if url in saved:
            return saved[url]
        else:
            page = func(url)
            saved[url] = page
            return page

    return wrapper

@cache
def web_lookup(url):
    return requests.get(url)

if __name__ == '__main__':
    urls = ['http://www.opensimsim.com', 'http://www.google.com.au']
    for u in urls:
        print("Loading %s..." % u)
        content = web_lookup(u)
        print("size: %d" % len(content.content))
    print("complete")
