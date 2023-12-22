import os
from PIL import Image
# print(os.listdir("./images"))
dir_nm = "./supplier-data/images/"
file_list = os.listdir(dir_nm)
for num, file in enumerate(file_list):
    im = Image.open(dir_nm+file)
    nm = file.split(".")[0]
    im.resize((3000,2000)).save(dir_nm + nm +".tiff", format="TIFF")
