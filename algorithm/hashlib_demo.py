#!/usr/bin/env python
#-*- coding: utf-8 -*-

import hashlib

md5 = hashlib.md5()
md5.update('how to use md5 in python hashlib?'.encode('utf'))
md5.update('python hashlib?'.encode('utf'))
code = md5.hexdigest()
print("md5 -> code: %s, len: %d, bytes: %d" % (code, len(code), len(code) * 4))

sha1 = hashlib.sha1()
sha1.update('how to use sha1 in '.encode('utf'))
sha1.update('python hashlib?'.encode('utf'))
code = sha1.hexdigest()
print("sha1 -> code: %s, len: %d, bytes: %d" % (code, len(code), len(code) * 4))

sha256 = hashlib.sha256()
sha256.update('welcome to Python world'.encode('utf'))
code = sha256.hexdigest()
print("sha256 -> code: %s, len: %d, bytes: %d" % (code, len(code), len(code) * 4))

sha512 = hashlib.sha512()
sha512.update('welcome to Python world'.encode('utf'))
code = sha512.hexdigest()
print("sha512 -> code: %s, len: %d, bytes: %d" % (code, len(code), len(code) * 4))