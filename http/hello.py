#!/usr/bin/env python
#-*- coding: utf-8 -*-

def application(env, start_res):
    start_res('200 OK', [('Content-Type', 'text/html')])
    body = '<h1>Hello, %s!</h1>' % (env['PATH_INFO'][1:] or 'web')
    return [body.encode('utf')]
