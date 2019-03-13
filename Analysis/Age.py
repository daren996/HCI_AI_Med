"""
Analyze Info of Age.

Structure of dial.txt:
obj{"id": id, "dial": dial}
dial[{"time": time, "speaker": speaker, "content": content}, ...]
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import Utils
from matplotlib.font_manager import FontProperties


font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

source_path = "../DataSet/"
data_dgn = "dial_dgn.txt"
data_no_dgn = "dial_no_dgn.txt"
data_no_rst = "dial_no_rst.txt"

# Comparison between complete and uncompleted dialogues according ages
age_dgn = {'0~6岁': 0, '7~15岁': 0, '16~35岁': 0, '36~60岁': 0, '大于60岁': 0}
age_no_dgn = {'0~6岁': 0, '7~15岁': 0, '16~35岁': 0, '36~60岁': 0, '大于60岁': 0}
age_no_rst = {'0~6岁': 0, '7~15岁': 0, '16~35岁': 0, '36~60岁': 0, '大于60岁': 0}
with open(source_path + data_dgn, "r") as in_file:
    for line in in_file.readlines():
        obj = json.loads(line)
        rst = json.loads(obj["dial"][-1]["content"])
        if not rst["attachment_dict"]:
            print("ERROR no attachment_dict:", line)
            continue
        age = rst["attachment_dict"]["age_group"]
        if age not in Utils.age_group:
            print("ERROR irregular age:", age, line)
        if age not in age_dgn:
            age_dgn[age] = 0
        age_dgn[age] += 1
with open(source_path + data_no_dgn, "r") as in_file:
    for line in in_file.readlines():
        obj = json.loads(line)
        rst = json.loads(obj["dial"][-1]["content"])
        if not rst["attachment_dict"]:
            print("ERROR no attachment_dict:", line)
            continue
        age = rst["attachment_dict"]["age_group"]
        if age not in Utils.age_group:
            print("ERROR irregular age:", age, line)
        if age not in age_no_dgn:
            age_no_dgn[age] = 0
        age_no_dgn[age] += 1
with open(source_path + data_no_rst, "r") as in_file:
    for line in in_file.readlines():
        obj = json.loads(line)
        for _, dial in enumerate(obj["dial"]):
            if "年龄" in dial["content"]:
                age = Utils.age_num2group(int(obj["dial"][_ + 1]["content"][0:-1]))
                if age not in Utils.age_group:
                    print("ERROR irregular age:", age, line)
                if age not in age_no_rst:
                    age_no_rst[age] = 0
                age_no_rst[age] += 1
labels = [num[0] for num in age_no_rst.items()]
age_dgn = [num[1]+list(age_no_dgn.items())[_][1] for _, num in enumerate(age_dgn.items())]
age_no_rst = [num[1] for num in age_no_rst.items()]
ratio = [num/age_no_rst[_] for _, num in enumerate(age_dgn)]
bar_width = 0.3
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.bar(np.arange(5), age_dgn, label='complete', alpha=0.8, width=bar_width)
ax1.bar(np.arange(5) + bar_width, age_no_rst, label='uncompleted', alpha=0.8, width=bar_width)
ax1.set_xlabel('age')
ax1.set_ylabel('number')
ax1.set_title('Comparison between complete and uncompleted dialogues\nand their ratios at different ages')
plt.xticks(np.arange(5)+bar_width/2, labels, fontproperties=font)
for _, num_dgn in enumerate(age_dgn):
    plt.text(_-bar_width*0.5, num_dgn+1, '%s' % num_dgn)
    plt.text(_+bar_width*0.5, age_no_rst[_]+1, '%s' % age_no_rst[_])
ax1.set_ylim(0, 650)
ax1.legend(loc=2)
ax2 = ax1.twinx()
ax2.plot(np.arange(5), ratio, 'r*', label='ratio between the number of the\n complete and the uncompleted')
ax2.set_ylabel('ratio')
ax2.set_ylim(0, 6)
for _, ra in enumerate(ratio):
    plt.text(_, ra+0.1, '%.2f' % ra)
ax2.legend()
plt.show()

# query as others 代替别人询问
# age_group = {}
# age_0_6 = []
# age_60 = []
# age_7_15 = []
# with open(source_path + data_dgn, "r") as in_file:
#     for line in in_file.readlines():
#         obj = json.loads(line)
#         rst = json.loads(obj["dial"][-1]["content"])
#         if not rst["attachment_dict"]:
#             continue
#         age = rst["attachment_dict"]["age_group"]
#         if age == "0~6岁":
#             age_0_6.append(obj["dial"][3]["content"])
#         if age == "大于60岁":
#             age_60.append(obj["dial"][3]["content"])
#         if age == "7~15岁":
#             age_7_15.append(obj["dial"][3]["content"])
#         if age not in age_group:
#             age_group[age] = 0
#         age_group[age] += 1
# print(age_group)
# for c in age_0_6:
#     print(c)
# print("\n")
# for c in age_7_15:
#     print(c)
# print("\n")
# for c in age_60:
#     print(c)
