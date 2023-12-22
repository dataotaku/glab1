#! /usr/bin/env python3

import os
import requests
import json
import time

dir_nm = "./supplier-data/descriptions/"
flist = os.listdir(dir_nm)

url = "http://34.16.139.142/feedback/"
headers = {"Content-Type": 'application/json; charset=utf-8'}

for idx in range(len(flist)):
    with open(dir_nm + flist[idx], 'r') as fp:
        lines = fp.readlines()
        res_dict={}
        nm = flist[idx].split(".")[0]
        if len(lines) < 3:
            pass
        else:
            txt_list = []
            for num in range(len(lines)):
                if num == 0:
                    res_dict['name'] = lines[num].strip()
                elif num == 1:
                    res_dict['weight'] = lines[num].strip()
                else:
                    txt_list.append(lines[num].strip())

        res_dict['description'] = " ".join(txt_list)
        res_dict['image_name'] = nm + ".jpeg"

    response = requests.post(url, data=json.dumps(res_dict), headers=headers)

    print(response.status_code)
    print(response.request.url)
    print(response.text)
    time.sleep(5)