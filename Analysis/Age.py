

import json
import numpy as np
import matplotlib.pyplot as plt

source_path = "../DataSet/"
data_set = "dial_dgn.txt"
rst_file_name = "rst.txt"


age_group = {}
age_0_6 = []
age_60 = []
age_7_15 = []
with open(source_path + data_set, "r") as in_file:
    for line in in_file.readlines():
        obj = json.loads(line)
        rst = json.loads(obj["dial"][-1]["content"])
        if not rst["attachment_dict"]:
            continue
        age = rst["attachment_dict"]["age_group"]
        if age == "0~6岁":
            age_0_6.append(obj["dial"][3]["content"])
        if age == "大于60岁":
            age_60.append(obj["dial"][3]["content"])
        if age == "7~15岁":
            age_7_15.append(obj["dial"][3]["content"])
        if age not in age_group:
            age_group[age] = 0
        age_group[age] += 1
print(age_group)
# for c in age_0_6:
#     print(c)
# print("\n")
for c in age_7_15:
    print(c)
# print("\n")
# for c in age_60:
#     print(c)


