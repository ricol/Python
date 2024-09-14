#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import json

app_id = "23a89c87"
app_key = "bdc75325d9d9ea4aa006d39fc83d72f2"
language = "en-gb"
word_id = "example"
url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word_id.lower()
r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
print("code {}\n".format(r.status_code))
print("json \n" + json.dumps(r.json()))