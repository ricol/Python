#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests as r

print("looking up your ip...")
response = r.get('https://httpbin.org/ip')
print("Your IP is {0}".format(response.json()['origin']))