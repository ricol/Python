#!/usr/bin/env python
#-*- coding: utf-8 -*-

import logging
logging.basicConfig(level=logging.INFO)
import asyncio, os, json, time
from datetime import datetime
from aiohttp import web

def index(request):
    return web.Response(body=b'<h1>Welcome to Python Web World!</h1>')

@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    ip = '127.0.0.1'
    port = 9000
    srv = yield from loop.create_server(app.make_handler(), ip, port)
    logging.info('server started at https://%s:%d' % (ip, port))
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
print("server end.")