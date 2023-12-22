import os
from PIL import Image
# print(os.listdir("./images"))
file_list = os.listdir("./images")
for num, file in enumerate(file_list):
    im = Image.open("./images/"+file)
    im.rotate(-90).resize((192,192)).save("./images/sample_"+str(num)+".tiff")
