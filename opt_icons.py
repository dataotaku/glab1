#!/usr/bin/env python
import os
from PIL import Image
# print(os.listdir("./images"))
file_list = os.listdir("./images")
for num, file in enumerate(file_list):
    im = Image.open("./images/"+file)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    nm = file.split(".")[0]
    # print(nm)
    im.rotate(90).resize((128,128)).save("./opt_icons/"+nm+".jpeg", format="JPEG")

print(os.listdir("./opt_icons"))



