#!/usr/bin/env python
#-*- coding: utf-8 -*-

import subprocess

print("% nslookup www.python.org")
r = subprocess.call(['nslookup', 'www.python.org'])
print("Exit code: %d" % (r))