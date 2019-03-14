
"""
Analyze Info of Genders.

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


# Comparison between complete and uncompleted dialogues according genders
gender_dgn = {'男': 0, '女': 0}
gender_no_dgn = {'男': 0, '女': 0}
gender_no_rst = {'男': 0, '女': 0}
with open(source_path + data_dgn, "r") as in_file:
    for line in in_file.readlines():
        obj = json.loads(line)
        rst = json.loads(obj["dial"][-1]["content"])
        if not rst["attachment_dict"]:
            print("ERROR no attachment_dict:", line)
            continue
        gender = rst["attachment_dict"]["gender"]
        if gender not in ["男", "女"]:
            print("ERROR irregular gender:", gender, line)
        if gender not in gender_dgn:
            gender_dgn[gender] = 0
        gender_dgn[gender] += 1
with open(source_path + data_no_dgn, "r") as in_file:
    for line in in_file.readlines():
        obj = json.loads(line)
        rst = json.loads(obj["dial"][-1]["content"])
        if not rst["attachment_dict"]:
            print("ERROR no attachment_dict:", line)
            continue
        gender = rst["attachment_dict"]["gender"]
        if gender not in ["男", "女"]:
            print("ERROR irregular gender:", gender, line)
        if gender not in gender_no_dgn:
            gender_no_dgn[gender] = 0
        gender_no_dgn[gender] += 1
with open(source_path + data_no_rst, "r") as in_file:
    for line in in_file.readlines():
        obj = json.loads(line)
        has_gender = False
        for _, dial in enumerate(obj["dial"]):
            if "性别" in dial["content"]:
                gender = obj["dial"][_ + 1]["content"]
                if gender not in ["男", "女"]:
                    print("ERROR irregular gender:", gender, line)
                if gender not in gender_no_rst:
                    gender_no_rst[gender] = 0
                gender_no_rst[gender] += 1
                has_gender = True
        if not has_gender:
            print("ERROR no gender:", line)
print(gender_dgn, gender_no_dgn, gender_no_rst)
labels = [num[0] for num in gender_no_rst.items()]
gender_dgn = [num[1]+list(gender_no_dgn.items())[_][1] for _, num in enumerate(gender_dgn.items())]
gender_no_rst = [num[1] for num in gender_no_rst.items()]
ratio = [num/gender_no_rst[_] for _, num in enumerate(gender_dgn)]
bar_width = 0.3
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.bar(np.arange(2), gender_dgn, label='complete', alpha=0.8, width=bar_width)
ax1.bar(np.arange(2) + bar_width, gender_no_rst, label='uncompleted', alpha=0.8, width=bar_width)
ax1.set_xlabel('gender')
ax1.set_ylabel('number')
ax1.set_title('Comparison between complete and uncompleted dialogues\nand their ratios at genders')
plt.xticks(np.arange(2)+bar_width/2, labels, fontproperties=font)
for _, num_dgn in enumerate(gender_dgn):
    plt.text(_-bar_width*0.5, num_dgn+1, '%s' % num_dgn)
    plt.text(_+bar_width*0.5, gender_no_rst[_]+1, '%s' % gender_no_rst[_])
ax1.set_ylim(0, 650)
ax1.legend(loc=2)
ax2 = ax1.twinx()
ax2.plot(np.arange(2)+bar_width/2, ratio, 'r*', label='ratio between the number of the\n complete and the uncompleted')
ax2.set_ylabel('ratio')
ax2.set_ylim(0, 6)
for _, ra in enumerate(ratio):
    plt.text(_+bar_width/2, ra+0.1, '%.2f' % ra)
ax2.legend()
plt.show()
