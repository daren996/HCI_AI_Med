"""
The occurrence time of each dialogue

Structure of dial.txt:
obj{"id": id, "dial": dial}
dial[{"time": time, "speaker": speaker, "content": content}, ...]
"""

import Utils
import json
import matplotlib.pylab as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import math
from collections import Counter
import csv
from scipy import interpolate

font = FontProperties(fname='/System/Library/Fonts/PingFang.ttc')
# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 9

source_path = "../DataSet/"
data_set = "dial.txt"
data_dgn = "dial_dgn.txt"
data_no_dgn = "dial_no_dgn.txt"
data_no_rst = "dial_no_rst.txt"

# get occurrence time distribution
# time_group = {'morning(6-12)': 0, 'afternoon(12-19)': 0, 'evening(19-23)': 0, 'night(23-6*)': 0}
# with open(source_path + data_set, "r") as in_file:
#     for line in in_file.readlines():
#         obj = json.loads(line)
#         if len(obj["dial"]) > 0:
#             tim = Utils.get_time_group(obj["dial"][0]["time"][1])
#             if tim not in time_group:
#                 time_group[tim] = 0
#             time_group[tim] += 1
# print(time_group)
# labels = [tim[0] for tim in time_group.items()]
# plt.bar(np.arange(4), [tim[1] for tim in time_group.items()])
# plt.xticks(np.arange(4), labels)
# plt.xlabel('time')
# plt.ylabel('number')
# plt.title('distribution of occurrence times of each dialogue')
# plt.show()

# gender distribution over time
# time_group_male = {'morning(6-12)': 0, 'afternoon(12-19)': 0, 'evening(19-23)': 0, 'night(23-6*)': 0}
# time_group_female = {'morning(6-12)': 0, 'afternoon(12-19)': 0, 'evening(19-23)': 0, 'night(23-6*)': 0}
# time_group_unknown = {'morning(6-12)': 0, 'afternoon(12-19)': 0, 'evening(19-23)': 0, 'night(23-6*)': 0}
# with open(source_path + data_set, "r") as in_file:
#     for line in in_file.readlines():
#         obj = json.loads(line)
#         if len(obj["dial"]) > 0:
#             gender = "未知"
#             if obj["dial"][-1]["speaker"] == "Robot":
#                 rst = json.loads(obj["dial"][-1]["content"])
#                 gender = rst["attachment_dict"]["gender"]
#             else:
#                 for _, dial in enumerate(obj["dial"]):
#                     if "性别" in dial["content"]:
#                         gender = obj["dial"][_ + 1]["content"]
#             tim = Utils.get_time_group(obj["dial"][0]["time"][1])
#             if gender == "男":
#                 if tim not in time_group_male:
#                     time_group_male[tim] = 0
#                 time_group_male[tim] += 1
#             if gender == "女":
#                 if tim not in time_group_female:
#                     time_group_female[tim] = 0
#                 time_group_female[tim] += 1
#             if gender == "未知":
#                 if tim not in time_group_unknown:
#                     time_group_unknown[tim] = 0
#                 time_group_unknown[tim] += 1
# labels = [num[0] for num in time_group_male.items()]
# tg_male = [num[1] for num in time_group_male.items()]
# tg_female = [num[1] for num in time_group_female.items()]
# ratio = [num/tg_female[_] for _, num in enumerate(tg_male)]
# bar_width = 0.3
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.bar(np.arange(len(tg_male)), tg_male, label='male', alpha=0.8, width=bar_width)
# ax1.bar(np.arange(len(tg_female)) + bar_width, tg_female, label='female', alpha=0.8, width=bar_width)
# ax1.set_xlabel('time')
# ax1.set_ylabel('number')
# ax1.set_title('Comparison between male and female dialogues\nand their ratios at different time')
# plt.xticks(np.arange(len(tg_male))+bar_width/2, labels, fontproperties=font)
# for _, num_dgn in enumerate(tg_male):
#     plt.text(_-bar_width*0.5, num_dgn+1, '%s' % num_dgn)
#     plt.text(_+bar_width*0.5, tg_female[_]+1, '%s' % tg_female[_])
# ax1.set_ylim(0, )
# ax1.legend(loc=2)
# ax2 = ax1.twinx()
# ax2.plot(np.arange(len(labels))+bar_width/2, ratio, 'r*', label='ratio between the number of\n the male and the female')
# ax2.set_ylabel('ratio')
# ax2.set_ylim(0.4, 1.6)
# for _, ra in enumerate(ratio):
#     plt.text(_+bar_width/2, ra+0.03, '%.2f' % ra)
# ax2.legend()
# plt.show()


# age distribution over time
time_group_arr = {}
for ag in Utils.age_group:
    time_group_arr[ag] = {'morning(6-12)': 0, 'afternoon(12-19)': 0, 'evening(19-23)': 0, 'night(23-6*)': 0}
time_group_unknown = {'morning(6-12)': 0, 'afternoon(12-19)': 0, 'evening(19-23)': 0, 'night(23-6*)': 0}
with open(source_path + data_set, "r") as in_file:
    for line in in_file.readlines():
        obj = json.loads(line)
        if len(obj["dial"]) > 0:
            age = "未知"
            if obj["dial"][-1]["speaker"] == "Robot":
                rst = json.loads(obj["dial"][-1]["content"])
                age = rst["attachment_dict"]["age_group"]
            else:
                for _, dial in enumerate(obj["dial"]):
                    if "年龄" in dial["content"]:
                        age_num = obj["dial"][_ + 1]["content"][0:-1]
                        age = Utils.age_num2group(int(age_num))
            tim = Utils.get_time_group(obj["dial"][0]["time"][1])
            for ag in Utils.age_group:
                if age == ag:
                    time_group_arr[age][tim] += 1
            if age == "未知":
                if tim not in time_group_unknown:
                    time_group_unknown[tim] = 0
                time_group_unknown[tim] += 1
print(time_group_arr)
labels = [num[0] for num in time_group_arr[Utils.age_group[0]].items()]
tg_arr = {}
for ag in Utils.age_group:
    tg_arr[ag] = [num[1] for num in time_group_arr[ag].items()]
bar_width = 0.15
fig = plt.figure()
ax1 = fig.add_subplot(111)
for _, ag in enumerate(Utils.age_group):
    ax1.bar(np.arange(len(tg_arr[ag]))+bar_width*_, tg_arr[ag], label=Utils.age_decode[ag], alpha=0.8, width=bar_width)
ax1.set_xlabel('time')
ax1.set_ylabel('number')
ax1.set_title('Comparison between dialogues of different ages\nand their ratios at different time')
plt.xticks(np.arange(len(tg_arr[Utils.age_group[0]]))+bar_width*2, labels, fontproperties=font)
for _, num in enumerate(tg_arr[Utils.age_group[0]]):
    for __, ag in enumerate(Utils.age_group):
        plt.text(_+bar_width*(__-0.5), tg_arr[ag][_]+1, '%s' % tg_arr[ag][_])
ax1.set_ylim(0, )
ax1.legend(loc=2)
plt.show()

