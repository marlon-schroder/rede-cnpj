#!/usr/bin/env python3

import requests
import dateutil.parser

url = "http://200.152.38.155/CNPJ/Cnaes.zip"

response = requests.head(url)
remote_timestamp = response.headers.get("Last-Modified")
if remote_timestamp:
    remote_timestamp = dateutil.parser.parse(remote_timestamp)
    remote_timestamp = remote_timestamp.strftime("%Y%m%d")
    print(remote_timestamp)


import os
import time

local_file = "./dados-publicos-zip/Cnaes.zip"

ti_c = os.path.getctime(local_file)
c_ti = time.ctime(ti_c)

# Using the timestamp string to create a time object/structure
t_obj = time.strptime(c_ti)

# Transform the time object to a date format timestamp
local_timestamp = time.strftime("%Y%m%d", t_obj)

print(local_timestamp)


if int(remote_timestamp) > int(local_timestamp):
    print("atualizo a base")
