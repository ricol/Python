#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import hashlib
import urllib.request
import requests
import json
import urllib
import random

def md5(s):
    m = hashlib.md5(s.encode('utf-8'))
    return m.hexdigest()

def push_unicast(appkey, app_master_secret, device_token):
    timestamp = int(time.time()*1000)
    method ="POST"
    url ="http://msg.umeng.com/api/send"
    params ={
                "appkey": appkey,
                "timestamp": timestamp,
                "device_tokens": device_token,
                "type":"listcast",
# ========================消息体===========================
                "payload":{
                    "aps":{
                        "alert":"abc",
                        #"badge":100,
                        # "content-available":1
                        #"recall": "uu07360151565675199411"
                    }
                },
# ========================消息体===========================
                "production_mode":"false"
            }
    post_body = json.dumps(params).encode("utf-8")
    print(post_body)
    sign = md5("%s%s%s%s"%(method,url,post_body,app_master_secret))
    req = urllib.request.Request(url +"?sign="+sign)
    try:
        r = urllib.request.urlopen(req, data=post_body)
        print(r.read())
    except urllib.error.URLError as e1:
        print("URL error: " + str(e1) + ", reason: " + str(e1.reason))
    except urllib.error.HTTPError as e2:
        print("HTTPError: " + str(e2) + ", reason: " + str(e1.reason))

if __name__ =="__main__":
    appkey =""
    app_master_secret =""
    device_token =""
    # 34b74d65-57da-41a1-b8b0-2be9d6700dc2
    push_unicast(appkey, app_master_secret, device_token)