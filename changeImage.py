import os
from PIL import Image
dir_nm = "./supplier-data/images/"
file_list = os.listdir(dir_nm)
for num, file in enumerate(file_list):
    im = Image.open(dir_nm+file)
    nm = file.split(".")[0]
    im.resize((600,400)).save(dir_nm + nm +".jpeg", format="JPEG")