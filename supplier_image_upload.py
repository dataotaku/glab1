#! /usr/bin/env python3
import os
import requests
import time

# file 업로딩 using python requests module

url = "http://localhost/upload/"

dir_nm = "./supplier-data/images/"
jpg_list = [ x for x  in os.listdir(dir_nm) if x.endswith(".jpeg")]
print(jpg_list)

for jpg in jpg_list:
    with open(dir_nm + jpg, "rb") as opened:
        r = requests.post(url, files={'file': opened})
        print(r.text)
        time.sleep(5)
