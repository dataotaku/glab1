# 예제파일을 텍스트 파일로 바꾸는 방법.
import os
import json

mid_data = []
with open("./data/renttherunway_final_data.json", "r") as data:
    for line in data:
        mid_data.append(json.loads(line))

len(mid_data)
print(mid_data[0:2])

full_array = []
for elem in mid_data[0:30]:
    txt = elem
    my_dict = {}
    for key, item in txt.items():
        if key in ('review_summary'):
            my_dict['title'] = item
        elif key in ('user_id'):
            my_dict['name'] = item
        elif key in ('review_date'):
            my_dict['date'] = item
        elif key in ('review_text'):
            my_dict['feedback'] = item
    full_array.append(my_dict)

for elem in full_array:
    for key, item in elem.items():
        print((key, item))

print(len(full_array))

for elem in range(len(full_array)):
    print(elem)
    #print(type(elem))
    dum_data = full_array[elem]
    print(dum_data)
    with open("./data/feedback/"+f'{elem+1:03d}'+".txt", "w") as txt_file:
        for name in ["title","name","date","feedback"]:
            if name != "feedback":
                txt_file.write(dum_data[name] + "\n")
            else:
                txt_file.write(dum_data[name])


################
# My solution
######################


flist = os.listdir("./data/feedback")
for idx in range(len(flist)):
    with open("./data/feedback/"+flist[idx], 'r') as fp:
        lines = fp.readlines()
        res_dict={}
        if len(lines) < 4:
            pass
        else:
            txt_list = []
            for num in range(len(lines)):
                if num == 0:
                    res_dict['title'] = lines[num].strip()
                elif num == 1:
                    res_dict['name'] = lines[num].strip()
                elif num == 2:
                    res_dict['date'] = lines[num].strip()
                else:
                    txt_list.append(lines[num].strip())

            res_dict['feedback'] = " ".join(txt_list)

    print(res_dict)

            










